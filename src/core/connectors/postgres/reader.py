"""
  Description:    Postgres Reader
"""

import time
import logging
from collections import OrderedDict
import json
import itertools
import psycopg2

from core.general.exceptions import SIDException


class Reader:
    """
        Postgres Reader
    """

    def __init__(self, *args, **kwargs):
        self.client = None
        self.user_id = None
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
            connect to postgres
        """
        from core.connectors.postgres.client import PostgresClient
        self.client = PostgresClient().getclient(self.config.conn_object)

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
        logging.debug('Execute Postgres Reader')
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
                yield record

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

    def query_all(self, sql_string):
        """
            query postgres
        """
        logging.debug("Query: " + sql_string)
        try:
            self.cursor.execute(sql_string)
        except psycopg2.Error as err:
            logging.error(err.diag.message_primary)
            raise SIDException(err.diag.message_primary)
        return self.cursor.fetchall()

    def query_with_param(self, sql_string, param):
        logging.debug("Query: " + sql_string)
        try:
            self.cursor.execute(sql_string, tuple(param))
        except psycopg2.Error as err:
            logging.error(err.diag.message_primary)

            raise SIDException(err.diag.message_primary)
        return self.cursor.fetchall()

    def down(self):
        """
            clean up
        """
        pass
