"""
  Description:    Salesforce Reader
"""

import time
import logging
from collections import OrderedDict
import json
import itertools

from simple_salesforce.exceptions import SalesforceExpiredSession
from simple_salesforce.exceptions import SalesforceGeneralError
from simple_salesforce.exceptions import SalesforceMalformedRequest
from simple_salesforce.exceptions import SalesforceRefusedRequest
from simple_salesforce.exceptions import SalesforceResourceNotFound
from simple_salesforce.exceptions import SalesforceError

from core.general.exceptions import SIDException


class Reader:
    """
        Salesforce Reader
    """

    def __init__(self, *args, **kwargs):
        self.sfclient = None
        self.user_id = None
        self.query_results = []
        self.header_fields = []
        self.normalize = False
        self.field_sep = '->'

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
        logging.debug("Reader: setup")

        self.connect()
        return self.set_reader()

    def connect(self):
        """
            connect to salesforce
        """
        from core.connectors.salesforce.client import SalesforceClient
        sfclient = SalesforceClient()
        self.sfclient = sfclient.getclient(self.config.conn_object)

    def set_reader(self):
        """
            reader fetchs all the records and
            returns one record at a time
            query: input query format is
            {
                rawquery: <original query>,
                metadata: metadata about query
            }
        """
        logging.debug('Execute Salesforce Reader')
        query = self.config.query.get('query', None)
        if not query:
            SIDException('Invalid query')

        metadata = self.config.query.get('metadata', None)
        if metadata:
            self.get_header(metadata)

        self.query_results = self.query_all(query)
        if self.query_results:
            return True

        return False

    def read(self):
        """
            iterate through records
        """
        try:
            for record in self.query_results:
                record = self.strip_unwanted_keys(record)
                record = json.loads(json.dumps(record))

                if not self.normalize:
                    yield record
                else:
                    """
                        normalize
                    """
                    records = self.normalise_record(record)
                    for record in records:
                        record = self.map_record(record)
                        yield record

        except (SalesforceExpiredSession,
                SalesforceGeneralError,
                SalesforceRefusedRequest,
                SalesforceResourceNotFound,
                SalesforceError) as sexp:
            raise SIDException(str(sexp.content))
        except SalesforceMalformedRequest as sexp:
            raise SIDException(str(sexp.content))
        except Exception as exp:
            logging.error('Error processing query')
            raise SIDException(str(exp))

    @property
    def header(self):
        """
            return header fields
        """
        return self.header_fields

    @property
    def input_object(self):
        if self.query_results:
            return 'query'
        return None

    def get_header(self, metadata):
        """
            get fields structure from query
        """
        if not metadata:
            SIDException('Invalid metadata input')

        fields = self.get_fields(metadata)
        for field in fields:
            rec = {
                'field_name': field,
                'field_type': 'Auto',
                'field_length': None,
                'label': None,
                'primary_key': None,
                'choices': None,
                'nullable': None,
                'model_name': 'query'
            }
            self.header_fields.append(rec)

    def get_fields(self, metadata):
        """
            from query structure find all the fields
        """
        ofields = []
        if not isinstance(metadata, dict):
            raise SIDException('Invalid Metadata')

        model = metadata.get('fields', None)
        if not model:
            raise SIDException('Invalid Metadata')

        for struc in model:
            ftype = struc.get('type', None)
            if not ftype:
                continue
            alias = struc.get('alias', None)

            if ftype == 'Field':
                if alias:
                    ofields.append(alias)
                else:
                    val = struc.get('field', None)
                    if not val:
                        raise SIDException('Field Missing')
                    ofields.append(val)
            elif ftype == 'FieldSubquery':
                subquery = struc.get('subquery', None)
                if not subquery:
                    raise SIDException('Invalid subquery')

                subrelation = subquery.get('relationshipName', None)
                if not subrelation:
                    raise SIDException('Invalid Subquery Relationship')

                subfields = self.get_fields(subquery)
                if not subfields:
                    raise SIDException('Invalid Subquery fields')
                for sfield in subfields:
                    nsfield = subrelation + self.field_sep + sfield
                    ofields.append(nsfield)
            elif ftype == 'FieldFunctionExpression':
                if not alias:
                    raise SIDException('aliaas for function is missing')
                ofields.append(alias)
            elif struc['type'] == 'FieldRelationship':
                if alias:
                    ofields.append(alias)
                else:
                    val = struc.get('rawValue', None)
                    if not val:
                        raise SIDException('Invalid Relationship field')
                    ofields.append(val)
            elif ftype in ['FieldTypeof', 'WHEN']:
                raise SIDException('Query type not Supported')
            else:
                raise SIDException('Invalid Query')

        return ofields

    def query_all(self, query, iter_flag=True):
        """
            query all records
        """

        try:
            if iter_flag:
                results = self.sfclient.query_all_iter(query)
                return results
            else:
                results = self.sfclient.query_all(query)
                return results

        except (SalesforceExpiredSession,
                SalesforceMalformedRequest,
                SalesforceRefusedRequest,
                SalesforceResourceNotFound,
                SalesforceError) as sexp:
            raise SIDException(str(sexp))
        except SalesforceGeneralError as sexp:
            """
                something went wrong...
                let's run the query again
            """
            time.sleep(10)
            logging.debug(
                'Salesforce General Exception... Rerunning the query')
            try:
                results = self.sfclient.query_all(query)
                return results
            except Exception:
                raise SIDException(str(sexp))
        except Exception as exp:
            logging.error('Error processing query')
            raise SIDException(str(exp))

    def strip_unwanted_keys(self, structure):
        """
            https://github.com/simple-salesforce/simple-salesforce/issues/283
        """
        def fixdict(
                struc, keyChainList, parentListRecord,
                parentListAddColsAndVals, parentListKillCols, passingContext):
            if 'records' in struc.keys() and type(struc['records']) is list:
                parentListRecord[keyChainList[0]] = struc['records']
                fixlist(parentListRecord[keyChainList[0]], 'fixDict')
            else:
                if 'attributes' in struc.keys():
                    struc.pop('attributes')
                for k in struc.keys():
                    if k != 'attributes':
                        if type(struc[k]) in [dict, OrderedDict]:
                            parentListAddColsAndVals, parentListKillCols = fixdict(
                                struc[k], keyChainList + [k],
                                parentListRecord, parentListAddColsAndVals,
                                parentListKillCols, 'fixDict')
                        if type(struc[k]) not in [None, list, dict, OrderedDict] and len(keyChainList) > 0:
                            parentListAddColsAndVals['.'.join(
                                keyChainList + [k])] = struc[k]
                            if passingContext == 'fixDict':
                                parentListKillCols.add(keyChainList[0])
            return parentListAddColsAndVals, parentListKillCols

        def fixlist(struc, passingContext):
            if type(struc) is list and len(struc) > 0:
                for x in struc:
                    if type(x) in [dict, OrderedDict]:
                        listAddColsAndVals, listKillCols = fixdict(
                            x, [], x, {}, set(), 'fixList')
                        if len(listAddColsAndVals) > 0:
                            for k, v in listAddColsAndVals.items():
                                x[k] = v
                        if len(listKillCols) > 0:
                            for k in listKillCols:
                                if k in x.keys():
                                    x.pop(k)
            return
        outerStructure = [structure]
        if type(outerStructure) is list:
            fixlist(outerStructure, 'outermost')
        return outerStructure[0]

    # def normalise_record(self, record):
    #     """
    #         normalise the record
    #     """
    #     if isinstance(record, dict):
    #         keys = record.keys()
    #         values = (self.normalise_record(val) for val in record.values())
    #         for val in itertools.product(*values):
    #             yield (dict(zip(keys, val)))
    #     elif isinstance(record, list):
    #         if not record:
    #             yield None
    #         for rec in record:
    #             yield from self.normalise_record(rec)
    #     else:
    #         yield record

    def normalise_record(self, record):
        """
            normalise the record
        """
        normalized = []
        orig_rec_fields = {}
        sublist = []
        for key, value in record.items():
            if isinstance(value, list):
                sublist.append(key)
                continue
            orig_rec_fields[key] = value

        if not sublist:
            normalized.append(orig_rec_fields)
            return normalized

        for key in sublist:
            value = record[key]
            for subrec in value:
                subfields = {}
                for subkey, subvalue in subrec.items():
                    newkey = key + self.field_sep + subkey
                    subfields[newkey] = subvalue
                """
                    merge with orig_rec_fields
                """
                normalized.append(
                    self.map_fields(
                        {**orig_rec_fields, **subfields}
                    )
                )

        return normalized

    def map_fields(self, record):
        """
            map fields and add any missing fields
        """
        newrecord = {}
        for field in self.header_fields:
            fieldname = field.get('field_name', None)
            if not fieldname:
                continue
            newrecord[fieldname] = record.get(fieldname, None)
            # if fieldname not in record.keys():
            #     record[fieldname] = None
        return newrecord

    def map_record(self, record):
        """
            map record to field structure
        """
        newrecord = {}
        for key, value in record.items():
            if not isinstance(value, dict):
                newrecord[key] = value
            else:
                for skey, sval in value.items():
                    nkey = key + self.field_sep + skey
                    newrecord[nkey] = sval

        return self.map_fields(newrecord)

    def down(self):
        """
            clean up
        """
        pass
