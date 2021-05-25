"""
  Description:    Connector Mapper
"""

from datetime import date
import logging

from django.db import transaction
from django.utils import timezone
from core.general.exceptions import SIDException

class ConnectorMapper():
    """
        Connector Mapper
    """

    def __init__(self, *args, **kwargs):
        self.object_id = None
        self.connector = None

        allowed_fields = set(['user_id', 'name', 'conn_name',
                              'conn_usage', 'conn_system_type'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field].strip())
            except Exception:
                setattr(self, field, None)

    def map(self):
        """
            let's map the output
            when called from django api please set user_id to user from request
        """
        logging.debug('Connector Mapper')
        dim_conn_name = None
        dim_system_type = None

        if not self.user_id:
            """
                make sure user is populated
            """
            raise SIDException('Mandatory Field Missing', 'User')

        from core.models.coreproxy import ConnectorProxy, ObjectProxy
        object_record = None

        if self.object_id:
            """
                we have connector object which means its an update
            """
            self.connector = self.getconnector()
        else:
            """
                check if we can find the connector object
            """
            if not self.name or not self.conn_name or \
                    not self.conn_system_type:
                raise SIDException('Mandatory Field Missing', 'name/type')

            # self.connector = ConnectorProxy.objects.get_or_none(
            #     name=self.name
            # ).select_related()
            """
                unfortunately cant use proxy get_or_none with select_related
            """
            recs = ConnectorProxy.objects.select_related('object').filter(
                name=self.name,
                object__object_owner=self.user_id
            )
            if recs:
                self.connector = recs[0]
        """
            check connector type
        """
        from core.models.coreproxy import DimConnectorProxy, DimSystemTypeProxy

        dim_conn_name = DimConnectorProxy.objects.get_or_none(
            conn_name=self.conn_name
        )
        if not dim_conn_name:
            raise SIDException('Invalid Field', 'connectortype')

        dim_system_type = DimSystemTypeProxy.objects.get_or_none(
            system_type=self.conn_system_type
        )
        if not dim_system_type:
            raise SIDException('Invalid Field', 'systemtype')

        """
            if connector is not available then create a new one
        """

        if not self.connector:

            object_record = ObjectProxy(
                sys_creation_date=timezone.now(),
                user_id=self.user_id,
                object_type='Connector',
                object_key=self.name,
                object_owner=self.user_id,
                effective_date=timezone.now(),
                expiration_date=date(4999, 12, 31)
            )

            self.connector = ConnectorProxy(
                sys_creation_date=timezone.now(),
                user_id=self.user_id,
                object=object_record,
                name=self.name,
                conn_name=dim_conn_name,
                conn_system_type=dim_system_type
            )
        else:
            self.connector.sys_update_date = timezone.now()
            self.connector.user_id = self.user_id
            self.connector.conn_name = dim_conn_name
            self.connector.conn_system_type = dim_system_type
            object_record = self.connector.object

        """
            check if the user has permission to object
        """
        if object_record.object_owner not in [self.user_id, 'admin']:
            raise SIDException('Permission denied', 'object')

        try:
            with transaction.atomic():
                object_record.save()
                self.connector.object = object_record
                self.connector.save()
        except Exception:
            transaction.rollback()
            raise SIDException('Error storing in database', 'object')

    def getconnector(self):
        """
            fetch the connector based on object_id
        """
        from core.models.coreproxy import ConnectorProxy

        if self.object_id:
            """
                we have connector object which means its an update
            """
            self.connector = ConnectorProxy.objects.get_or_none(
                object_id=self.object_id)
            return self.connector

        return None

    def mapmodels(self, modellist):
        """
            get the model list and map that to dmodel
        """
        if not modellist:
            modellist = []
        from core.models.coreproxy import DmodelsProxy

        try:
            with transaction.atomic():
                # DmodelsProxy.objects.filter(
                #     conn_object_id=self.connector.object.object_id
                # ).delete()
                """
                    we remove object
                """
                for model in modellist:
                    model_name = model['name']
                    if not model_name or len(model_name.strip()) < 1:
                        continue
                    model_name = model_name.strip()
                    """
                        save each model
                        first we check if the object exists
                    """
                    recs = DmodelsProxy.objects.filter(
                        conn_object_id=self.connector.object.object_id,
                        name=model_name)
                    if recs:
                        dmodel = recs[0]
                        dmodel.sys_update_date = timezone.now()
                        dmodel.user_id = self.user_id
                        dmodel.label = model['label']
                        dmodel.readable = model['readable']
                        dmodel.writeable = model['writeable']
                    else:
                        dmodel = DmodelsProxy(
                            sys_creation_date=timezone.now(),
                            user_id=self.user_id,
                            conn_object=self.connector,
                            name=model_name,
                            label=model['label'],
                            readable=model['readable'],
                            writeable=model['writeable']
                        )
                    dmodel.save()

        except Exception:
            transaction.rollback()
            raise SIDException('Error storing in database', 'object')

    def mapfields(self, model_name, fieldlist):
        """
            get the model list and map that to dmodel
        """
        if not fieldlist:
            fieldlist = []

        if not self.connector or not self.user_id:
            raise SIDException('Mandatory Field Missing', 'Connector / User')

        from core.models.coreproxy import DmodelsProxy, FieldsProxy

        model_rec = DmodelsProxy.objects.get_or_none(
            conn_object_id=self.connector.object.object_id,
            name=model_name)
        if not model_rec:
            raise SIDException('Model not Found', model_name)

        try:
            with transaction.atomic():
                # DmodelsProxy.objects.filter(
                #     conn_object_id=self.connector.object.object_id
                # ).delete()
                """
                    we remove object
                """
                for field in fieldlist:
                    field_name = field['field_name']
                    if not field_name or len(field_name.strip()) < 1:
                        continue
                    field_name = field_name.strip()

                    """
                        save each model
                        first we check if the object exists
                    """
                    frecord = FieldsProxy.objects.get_or_none(
                        model__conn_object_id=model_rec.conn_object_id,
                        model__name=model_name,
                        field_name=field_name)
                    if frecord:
                        frecord.sys_update_date = timezone.now()
                        frecord.user_id = self.user_id
                        frecord.field_name = field_name
                        frecord.field_type = field['field_type']
                        frecord.field_length = field['field_length']
                        frecord.label = field['label']
                        frecord.primary_key = field['primary_key']
                        frecord.choices = field['choices']
                        frecord.nullable = field['nullable']

                    else:
                        frecord = FieldsProxy(
                            sys_creation_date=timezone.now(),
                            user_id=self.user_id,
                            model=model_rec,
                            field_name=field_name,
                            field_type=field['field_type'],
                            field_length=field['field_length'],
                            label=field['label'],
                            primary_key=field['primary_key'],
                            choices=field['choices'],
                            nullable=field['nullable']

                        )
                    frecord.save()

        except Exception:
            transaction.rollback()
            raise SIDException('Error storing in database', 'object')
