"""
  Description:    Salesforce client
"""

import logging
from datetime import datetime
from django.db.models import Q

from simple_salesforce.exceptions import SalesforceExpiredSession
from simple_salesforce.exceptions import SalesforceGeneralError
from simple_salesforce.exceptions import SalesforceMalformedRequest
from simple_salesforce.exceptions import SalesforceRefusedRequest
from simple_salesforce.exceptions import SalesforceResourceNotFound
from simple_salesforce.exceptions import SalesforceError

from simple_salesforce import Salesforce
from core.general.exceptions import SIDException


class SalesforceClient():
    """
        The class responsiblities are:
            Setup connection with Salesforce and fetch the records
    """

    def __init__(self, *args, **kwargs):
        self.sfconn = None

    def authenticate(self,
                     username,
                     password,
                     secrettoken,
                     conn_system_type='test',
                     hostname=None,
                     auth_host=None):
        """
            get authentication setup
        """
        self.sfconn = None

        logging.debug('Authenticating user')
        try:
            self.sfconn = Salesforce(
                username=username,
                password=password,
                security_token=secrettoken,
                domain='test' if conn_system_type != 'Production' else None
            )

        except (SalesforceExpiredSession,
                SalesforceGeneralError,
                SalesforceMalformedRequest,
                SalesforceRefusedRequest,
                SalesforceResourceNotFound,
                SalesforceError
                ) as sexp:
            raise SIDException(str(sexp))

        except Exception as err:
            logging.error(str(err))
            raise SIDException("Salesforce Connection Error")

        logging.debug('Authenticate success')
        return self.sfconn

    def getclient(self, connector):
        """
            fetch the client
        """
        logging.debug('Connecting Salesforce..')
        from core.models.coreproxy import AuthSalesforceProxy
        if not connector:
            raise SIDException('connector missing', 'connector')

        auth_record = AuthSalesforceProxy.objects.get_or_none(
            conn_object_id=connector.object_id
        )
        if not auth_record:
            raise SIDException('auth client missing', 'Salesforce')
        """
            encrypt the data
        """
        from core.general.sidcrypt import SIDEncryption

        sid_crypt = SIDEncryption()
        username = sid_crypt.decrypt(auth_record.auth_username)
        password = sid_crypt.decrypt(auth_record.auth_password)
        secrettoken = sid_crypt.decrypt(auth_record.security_token)

        conn_system_type = connector.conn_system_type.system_type

        self.authenticate(
            username,
            password,
            secrettoken,
            conn_system_type
        )

        logging.debug('Connection to salesforce: success')
        return self.sfconn

    def getclientbyid(self, conn_id, user_id):
        """
            fetch the client
        """
        try:
            conn_id = int(conn_id)
        except Exception:
            raise SIDException('Connector not found', 'connector')

        """
            check if the user has permission for the connector
        """
        from core.models.coreproxy import ConnectorProxy
        query = Q(Q(object__object_owner=user_id) & Q(
            object__object_type='Connector') & Q(
                object_id=conn_id) & Q(
                    Q(object__expiration_date__gte=datetime.today()) | Q(
                        object__expiration_date__isnull=True)
        )
        )
        conn_recs = ConnectorProxy.objects.filter(query)
        if not conn_recs:
            raise SIDException('Connector not found', 'connector')

        connector = conn_recs[0]
        return self.getclient(connector)
