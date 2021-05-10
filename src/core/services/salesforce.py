"""
  Description:    Salesforce service
"""

from datetime import datetime
from django.db.models import Q

from core.general.exceptions import SIDException


class SalesforceService():
    """
        The class responsiblities are:
            Tree structure
    """

    def __init__(self, *args, **kwargs):
        self.conn_id = None
        self.connector = None
        self.user_id = None
        self.sfclient = None

    def setup(self):
        """
            check the input fields
        """
        if not self.conn_id or not self.user_id:
            """
                check connector / userid
            """
            raise SIDException('Mandatory Field Missing', 'connector / user')

        from core.connectors.salesforce.client import SalesforceClient
        salesforce_client = SalesforceClient()
        self.sfclient = salesforce_client.getclientbyid(
            self.conn_id,
            self.user_id)

    def getmodels(self):
        """
            get all model details
        """
        if not self.sfclient:
            raise SIDException('Error connecting to Salesforce', '')

        try:
            sfobjects = self.getdetails()
            if sfobjects:
                from core.mapper.connectormapper import ConnectorMapper
                connmapper = ConnectorMapper()
                connmapper.object_id = self.conn_id
                connmapper.user_id = self.user_id
                connmapper.getconnector()
                connmapper.mapmodels(sfobjects)
                for sfobject in sfobjects:
                    sffields = self.getfields(sfobject['name'])
                    if sffields:
                        connmapper.mapfields(
                            sfobject['name'],
                            sffields)

            return sfobjects
        except Exception:
            raise SIDException('Error fetching Salesforce objects', '')

    def getdetails(self):
        """
            get instance details
        """
        if not self.sfclient:
            raise SIDException('Error connecting to Salesforce', '')

        sfobjects = []
        metarecords = self.sfclient.describe()
        for sobj in metarecords['sobjects']:
            if sobj['keyPrefix'] is not None:
                """
                    we store name, label, readable, writeable
                """
                if not sobj['queryable'] or not sobj['queryable']:
                    continue

                record = {
                    'name': sobj['name'],
                    'label': sobj['label'],
                    'readable': str(sobj['queryable']),
                    'writeable': str(sobj['deletable'])

                }
                sfobjects.append(record)
        return sfobjects

    def getfields(self, object_name):
        """
            get object attributes
        """
        sffields = []
        if not object_name:
            raise SIDException('SF: Invalid Object name', object_name)

        if not self.sfclient:
            raise SIDException('Error connecting to Salesforce', '')

        fields = None
        try:
            metarecords = self.sfclient.__getattr__(object_name).describe()
            for item in metarecords.items():
                if item[0] == 'fields':
                    fields = item[1]

        except Exception:
            raise SIDException('SF: Invalid Object', object_name)

        for sobj in fields:
            record = {
                'field_name': sobj['name'],
                'field_type': sobj['type'],
                'field_length': str(sobj['length']),
                'label': sobj['label'],
                'primary_key': None,
                'choices': sobj['picklistValues'],
                'nullable': 'Y' if sobj['nillable'] else 'N'
            }
            sffields.append(record)
        return sffields
