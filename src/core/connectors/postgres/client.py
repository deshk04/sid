"""
  Description:    Salesforce client
"""

import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import NamedTupleConnection

from django.db.models import Q

from core.general.exceptions import SIDException


class PostgresClient():
    """
        The class responsiblities are:
            Setup connection with postgres and fetch the records
    """

    def __init__(self, *args, **kwargs):
        self.pgconn = None
        self.cursor = None

    def authenticate(self,
                     username,
                     password,
                     database,
                     hostname,
                     port=5432):
        """
            get authentication setup
        """
        self.pgconn = None

        connectString = "dbname='{0}' host='{1}' port='{2}' \
                        user='{3}' password='{4}'".format(
                        database, hostname, port,
                        username, password)

        logging.debug('Authenticating user')
        try:
            self.pgconn = psycopg2.connect(connectString)

        except Exception as err:
            logging.error(str(err))
            raise SIDException("Postgres Connection Error")
        self.pgconn.autocommit = True

        self.cursor = self.pgconn.cursor(
                        cursor_factory=psycopg2.extras.NamedTupleCursor)

        logging.debug('Authenticate success')
        return self.cursor

    def getclient(self, connector):
        """
            fetch the client
        """
        logging.debug('Connecting Postgres..')
        from core.models.coreproxy import AuthDatabaseProxy
        if not connector:
            raise SIDException('connector missing', 'connector')

        auth_record = AuthDatabaseProxy.objects.get_or_none(
            conn_object_id=connector.object_id
        )
        if not auth_record:
            raise SIDException('auth client missing', 'Postgres')
        """
            encrypt the data
        """
        from core.general.sidcrypt import SIDEncryption

        sid_crypt = SIDEncryption()
        username = sid_crypt.decrypt(auth_record.auth_username)
        password = sid_crypt.decrypt(auth_record.auth_password)
        database = sid_crypt.decrypt(auth_record.auth_database)

        hostname = connector.conn_system_type.auth_host

        self.authenticate(
            username,
            password,
            database,
            hostname
        )

        logging.debug('Connection to postgres: success')
        return self.cursor

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

    def commit(self):
        self.pgconn.commit()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.pgconn:
            self.pgconn.close()
