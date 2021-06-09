"""
  Description:    Salesforce Mapper
"""
import logging
from datetime import date

from core.general.exceptions import SIDException
from core.general.sidhelper import check_dateformat


class Mapper:
    """
        Salesforce Mapper
    """

    def __init__(self, *args, **kwargs):
        self.sfclient = None
        self.modelmapper = None
        self.sfoptimize = True
        self.sflookup_size = 0
        self.sflookup_recheck = True
        self.lookup_dict = {}
        self.map_hook = None
        self.cache_conn = None
        self.cache_loadcount = 50000

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self):
        """
            setup connection
        """
        logging.debug("Salesforce Mapper: setup")

        """
            set up redis
        """
        from core.controller.cachecontroller import CacheController
        self.cache_conn = CacheController(
            user_id=self.user_id
        )
        self.cache_conn.setup()

        self.set_sfreader()
        self.set_mapper()

        from apps.hook.maphook import MapHook
        self.map_hook = MapHook()

    def set_sfreader(self):
        """
            set salesforce reader
        """
        from core.connectors.salesforce.reader import Reader
        self.reader = Reader(
            user_id=self.user_id,
            run_date=self.run_date,
            config=self.config
        )
        self.reader.connect()

    def set_mapper(self):
        """
            set up properities
        """
        from core.mapper.modelmapper import ModelMapper
        self.modelmapper = ModelMapper(
            user_id=self.user_id,
            run_date=self.run_date,
            config=self.config
        )
        self.modelmapper.map()
        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        if sid_settings.getkeyvalue('SFOPTIMIZE') != 'Y':
            logging.debug('SFOPTIMIZE Flag is False')
            self.sfoptimize = False

        if sid_settings.getkeyvalue('SFLOOKUP_RECHECK') == 'Y':
            logging.debug('SFLOOKUP_RECHECK Flag is True')
            self.sflookup_recheck = True

        self.sflookup_size = sid_settings.getkeyvalue_as_num(
            'SFLOOKUP_FILESIZE')
        if not self.sflookup_size:
            self.sflookup_size = 0

        for model_map in self.modelmapper.model_maps:
            if model_map['map_type_id'] == 'lookup':
                """
                    fetch the lookup in one go...
                """
                query = "SELECT {0}, {1} FROM {2}".format(
                    model_map['lookup_return_field'],
                    model_map['lookup_join_field'],
                    model_map['lookup_model']
                )
                return_dict = {}
                """
                    check if the lookup_model is already fetched
                    first we generate a unique key for model
                """
                lkey = self.get_lkey(model_map)

                if self.cache_conn.key_exists(lkey):
                    return True

                logging.debug(query)

                try:
                    counter = 0
                    temp_dic = {}
                    results = self.reader.query_all(query, True)
                    for rec in results:
                        counter += 1
                        record = dict(rec.items())
                        if not model_map['lookup_join_field']:
                            continue
                        temp_dic[record[model_map['lookup_join_field']]] = record[model_map['lookup_return_field']]
                        if counter > self.cache_loadcount:
                            self.cache_conn.set_dict(
                                lkey,
                                temp_dic
                            )
                            temp_dic = {}
                            counter = 0
                            # pdb.set_trace()

                    if len(temp_dic) > 0:
                        self.cache_conn.set_dict(
                            lkey,
                            temp_dic
                        )

                except SIDException as sexp:
                    raise sexp
                except Exception as exp:
                    logging.error('Error processing lookup result')
                    logging.error(str(exp))
                    raise SIDException('Error processing lookup execute')

    def map(self, record):
        """
            write record
        """
        query_data = {}
        warning_data = []
        for key, ovalue in record.items():
            """
                we can one field from source mapped to multiple
                fields in destination
            """
            map_fields = self.modelmapper.search_mapfield(key)
            for map_field in map_fields:
                value = ovalue
                if map_field["map_type_id"] == "ignore":
                    continue

                """
                    SF doesnt like empty string for certain field
                    best to make it null
                """
                if not value or value == "":
                    value = None

                if map_field["map_type_id"] == "map":
                    """
                        check if the destination field is date
                        SF has condition that if date year is
                        greater than 3999 then make it NULL
                    """
                    field_rec = self.modelmapper.search_field(
                        "D", map_field["dest_field"])
                    if field_rec and field_rec["field_type"] in ["date"]:
                        """
                            we check if the date is > 3999
                        """
                        try:
                            if value:
                                return_date = check_dateformat(value)
                                if return_date and (return_date > date(3999, 1, 1) or return_date < date(1700, 12, 31)):
                                    value = None

                        except SIDException:
                            logging.debug(record)
                            logging.debug(key)
                            logging.error("Invalid date: %s for %s",
                                          str(value), str(key))

                elif map_field["map_type_id"] == "lookup":
                    """
                        fetch the lookup value
                    """
                    value = self.process_lookup(
                        map_field, key, value)
                    if not value:
                        lmsg = "lookup field missing: " + str(record)
                        wrec = {}
                        wrec["key"] = key
                        wrec["value"] = value
                        wrec["message"] = lmsg
                        warning_data.append(wrec)
                elif map_field["map_type_id"] == "map_n_hook":
                    try:
                        newvalue = self.map_hook.map(
                            self.modelmapper.model_maps[0].job_id, key, value
                        )
                        if newvalue:
                            value = newvalue
                    except Exception:
                        logging.error("Error in map_n_hook")

                else:
                    continue

                query_data[map_field["dest_field"]] = value

        """
            constant are handled outside as they dont
            map to any fields
        """
        constantlist = self.modelmapper.search_mapconstant()
        for crec in constantlist:
            """
                handle the constant fields
            """
            if crec["dest_field"] and crec["map_value"]:
                query_data[crec["dest_field"]] = crec["map_value"]

        return [query_data, warning_data]

    def get_lkey(self, model_map):
        """
            return unique key
        """
        lkey = str(self.config.conn_object.id)
        lkey += '_' + model_map['lookup_model'].lower()
        lkey += '_' + model_map['lookup_join_field'].lower()
        lkey += '_' + model_map['lookup_return_field'].lower()
        return lkey

    def process_lookup(self, map_field, key, value):
        """
            check if the data is already fetched or not
            if it is fetched then do dict based lookup
            else call sf_lookup
        """
        if not value:
            return value

        newvalue = None
        if self.sfoptimize:
            lkey = self.get_lkey(map_field)
            try:
                newvalue = self.cache_conn.get_key(lkey, value)
                if newvalue:
                    return newvalue

            except Exception:
                logging.error('Lookup dictionary not found')
                logging.debug(lkey)

        if self.sflookup_recheck:
            return self.sf_lookup(map_field, key, value)
        return newvalue

    def sf_lookup(self, map_field, key, value):
        """
            get look value from SF
            we assume the model and fields for lookup object is already fetched
        """
        logging.debug('Inside sf_lookup')

        model = map_field.get('lookup_model', None)
        join_field = map_field.get('lookup_join_field', None)
        return_field = map_field.get('lookup_return_field', None)
        if not model or not join_field or not return_field:
            raise SIDException('Looking config missing', key)

        query = "SELECT {0} FROM {1} WHERE {2} = '{3}'".format(
            return_field, model, join_field, value
        )
        logging.debug(query)

        try:
            results = self.reader.query_all(query, False)
            for reskey, resval in results.items():
                if reskey == 'records':
                    if resval:
                        resvalue = resval[0]
                        for rkey, rval in resvalue.items():
                            if rkey == return_field:
                                return rval
            return None

        except SIDException as sexp:
            raise sexp
        except Exception as exp:
            logging.error('Error processing lookup records: parsing result')
            msg = 'return_field: ' + str(return_field)
            msg += ' model: ' + str(model)
            msg += ' join_field: ' + str(join_field)
            msg += ' value: ' + str(value)
            logging.error(msg)
            logging.error(str(exp))
            raise SIDException('Error processing lookup')

    @property
    def destination_object(self):
        """
            return destination object
        """
        return self.modelmapper.dest_model

    def down(self):
        """
            close any open connection
            and process unprocessed records
        """
        pass
