"""
  Description:    Jobs Mapper
"""

from datetime import date
import logging

from django.db import transaction
from django.utils import timezone
from django.db.models import Q

from core.general import settings
from core.general.exceptions import SIDException


class JobsMapper():
    """
        Jobs Mapper
    """

    def __init__(self, *args, **kwargs):
        self.job = None
        self.source_config = None
        self.dest_config = None
        self.bulk_count = None
        self.parallel_count = 1

        allowed_fields = set(['user_id', 'job_name', 'run_type'])
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
        logging.debug('Jobs Mapper')
        job_record = None
        object_record = None

        if not self.user_id or not self.run_type:
            """
                make sure user / connector is populated
            """
            raise SIDException('Mandatory Field Missing', 'User / type')

        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        bulk_count = sid_settings.getkeyvalue_as_num('BULK_COUNT')
        try:
            int(bulk_count)
            self.bulk_count
        except Exception:
            self.bulk_count = settings.BULK_COUNT

        from core.models.coreproxy import JobsProxy, ObjectProxy

        if 'File' in self.run_type:
            """
                check if we can find the connector object
            """
            if not self.filepath or not self.filestartwith or \
                    not self.fileendwith or not self.delimiter:
                raise SIDException('Mandatory Field Missing', 'file')

        query = (Q(job__object_type='Job') & Q(job_name=self.job_name))
        if sid_settings.sidadmin != self.user_id:
            query = Q(Q(job__object_owner=self.user_id) & Q(
                job__object_type='Job') & Q(job_name=self.job_name)
            )

        job_records = JobsProxy.objects.select_related('job').filter(
            query
        )
        if job_records:
            job_record = job_records[0]

        # from django.db import connection
        # print(connection.queries[-1])

        if not job_record:

            object_record = ObjectProxy(
                sys_creation_date=timezone.now(),
                user_id=self.user_id,
                object_type='Job',
                object_key=self.job_name,
                object_owner=self.user_id,
                effective_date=timezone.now(),
                expiration_date=date(4999, 12, 31)
            )

            job_record = JobsProxy(
                sys_creation_date=timezone.now(),
                user_id=self.user_id,
                job=object_record,
                job_name=self.job_name,
                run_type=self.run_type,
                parallel_count=self.parallel_count
            )
        else:
            job_record.sys_update_date = timezone.now()
            job_record.job_name = self.job_name
            job_record.run_type = self.run_type
            object_record = job_record.job

        """
            check if the user has permission to object
        """
        if object_record.object_owner not in [self.user_id, 'admin']:
            raise SIDException('Permission denied', 'object')

        try:
            with transaction.atomic():
                object_record.save()
                job_record.job = object_record
                job_record.save()
                self.job = job_record
        except Exception:
            transaction.rollback()
            raise SIDException('Error storing in database', 'object')

    def mapconfig(self, rec_type, conn_object,
                  filepath, filestartwith,
                  fileendwith, filemask,
                  delimiter, encoding, lineterminator,
                  archivepath, key_field,
                  bulk_count, query=None):
        """
            let's map the source connector details
            Job should have 2 job_confi record
            1. source_connector
            2. Dest connector
        """
        if not rec_type or rec_type not in ['S', 'D']:
            """
                make sure user / connector is populated
            """
            raise SIDException('Mandatory Field Missing', 'rec type')

        if not conn_object or not self.job:
            """
                make sure user / connector is populated
            """
            raise SIDException('Mandatory Field Missing', 'connector/job')

        if conn_object.conn_name == 'File':
            """
                check if we can find the connector object
            """
            if not self.filepath or not self.filestartwith or \
                    not self.fileendwith:
                raise SIDException('Mandatory Field Missing', 'file')

        try:
            int(bulk_count)
        except Exception:
            bulk_count = settings.BULK_COUNT

        if not delimiter or delimiter not in ['|', ',']:
            delimiter = ','
        if not encoding:
            encoding = 'utf-8'
        if not lineterminator:
            lineterminator = '\n'

        from core.models.coreproxy import JobConfigProxy

        job_config = JobConfigProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            job=self.job,
            rec_type=rec_type,
            conn_object=conn_object,
            filepath=filepath,
            filestartwith=filestartwith,
            fileendwith=fileendwith,
            filemask=filemask,
            delimiter=delimiter,
            encoding=encoding,
            lineterminator=lineterminator,
            archivepath=archivepath,
            key_field=key_field,
            bulk_count=bulk_count,
            query=query
        )

        try:
            with transaction.atomic():
                JobConfigProxy.objects.filter(
                    job_id=self.job.job_id,
                    rec_type=rec_type
                ).delete()
                job_config.save()
        except Exception:
            transaction.rollback()
            raise SIDException('Error storing in database', 'object')
