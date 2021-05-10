"""
  Description:    Salesforce Mapper
"""
import logging

from core.general.exceptions import SIDException

class Mapper:
    """
        File Mapper
    """

    def __init__(self, *args, **kwargs):
        self.modelmapper = None
        self.map_hook = None

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
        logging.debug("File Mapper: setup")

        self.set_mapper()

        from apps.hook.maphook import MapHook
        self.map_hook = MapHook()

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
        try:
            self.modelmapper.map()
        except SIDException as exp:
            logging.error('Mapper details missing')
            self.modelmapper = None

    def map(self, record):
        """
            map records
        """
        """
            if model mapper found then map
            based on model_map rules
        """
        if self.modelmapper:
            return self.map_mapper(record)
        else:
            return self.map_withoutmapper(record)

    def map_mapper(self, record):
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
                    if empty string then make it null
                """
                if not value or value == "":
                    value = None

                if map_field["map_type_id"] == "map":
                    """
                        dest field map
                    """
                    pass

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

    def map_withoutmapper(self, record):
        """
            return the same input record as output
        """
        warning_data = []
        return [record, warning_data]

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
