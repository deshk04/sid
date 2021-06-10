"""
  Description:    Jobs Controller
"""
import logging
import ast

from datetime import datetime, date
from django.utils import timezone
from django.db.models import Q

from core.general import settings
from core.general.exceptions import SIDException

class JobController():
    """
        Jobs Controller
    """

    def __init__(self, *args, **kwargs):
        allowed_fields = set(['user_id', 'job_id', 'run_date'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

        if not self.user_id or not self.job_id or not self.run_date:
            raise SIDException('Mandatory Field Missing',
                               'User / job_id / run_date')

    def execute(self,
                schedule_id,
                schedulelog_id,
                rerun=False,
                mark_complete=False):
        """
            run the job
        """
        logging.debug('Starting Job: %s', str(self.job_id))
        success = True
        """
            let's get user settings
        """
        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        if not sid_settings.settings:
            """
                user settings missing
            """
            raise SIDException('User settings missing')

        """
            set up cache controller
        """
        from core.controller.cachecontroller import CacheController
        self.cache_conn = CacheController(
            user_id=self.user_id
        )

        job = self.get_job()
        """
            if mark as complete then make the job as success
        """
        from core.models.coreproxy import JobrunLogProxy
        """
            if rerun flag is set then we dont check if the job
            is already run
        """
        job_run = None
        if not rerun:
            """
                we check if the job is run
            """
            job_run = JobrunLogProxy.objects.filter(
                job=job,
                run_date=self.run_date,
                status__in=['Complete', 'Running']
            )
            if job_run:
                """
                    job has been successful before so dont run it
                """
                return [success, job, job_run]

        if mark_complete:
            logging.debug(' mark job as complete')
            job_run = self.get_joblog(job, 'Complete')
            job_run.message = 'Marked as complete'
            job_run.total_count = 0
            job_run.failure_count = 0
            job_run.success_count = 0

            job_run.save()
            return [success, job, job_run]

        """
                Let's run the job
        """
        job_run = JobrunLogProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            job=job,
            run_date=self.run_date,
            status='Running',
            filename=None,
            schedule_id=schedule_id,
            schedulelog_id=schedulelog_id,
            success_count=0,
            failure_count=0,
            warning_count=0,
            total_count=0
        )
        job_run.save()

        try:
            job_run = self.run_job(
                job, job_run, rerun
            )

        except SIDException as sexp:
            msg = str(sexp)
            job_run.status = 'Failure'
            job_run.message = msg
            success = False
        job_run.save()

        """
            call logcontroller
            which will send the log file via email if configured
        """
        from core.models.coreproxy import JobDistributionProxy
        from core.controller.logcontroller import LogController

        job_distribution = JobDistributionProxy.objects.get_or_none(
            job_id=job.job_id
        )
        if job_distribution and job_distribution.email_flag == 'Y':
            if job_distribution.tolist and '@' in job_distribution.tolist:
                tolist = job_distribution.tolist.split(',')
                cclist = None
                if job_distribution.cclist:
                    cclist = job_distribution.cclist.split(',')

                try:
                    log_controller = LogController(
                        user_id=self.user_id
                    )
                    log_controller.job = job
                    log_controller.jobrun = job_run
                    log_controller.execute()
                    message = log_controller.get_summary()
                    subject = log_controller.get_title()
                    if log_controller.log_file and settings.JOB_EMAIL:
                        """
                            we should email the file
                        """
                        from core.connectors.email import SIDEmail
                        with SIDEmail() as sidmail:
                            sidmail.toList = tolist
                            sidmail.cc_list = cclist
                            sidmail.send(subject, message,
                                         log_controller.log_file)

                except Exception:
                    logging.error('Error producing log file')

        return [success, job, job_run]

    def run_job(self,
                job,
                job_run,
                rerun=False):
        """
            run the job
        """
        logging.debug('Processing Regular Job: %s', job.job_name)

        job_run.message = 'Started...'
        job_run.status = 'Running'

        """
                Before we execute let's get config details
        """
        adhocFlag = False
        if job.run_type == 'A':
            adhocFlag = True
        source_config, dest_config = self.get_jobconfig(job.job_id, adhocFlag)
        return self.run_jobbyconfig(job, source_config, dest_config)

    def run_jobbyconfig(self,
                        job,
                        source_config,
                        dest_config
                        ):
        from core.models.coreproxy import JobrunLogProxy

        """
                Let's run the job
        """
        job_run = JobrunLogProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            job=job,
            run_date=self.run_date,
            status='Running',
            filename=None,
            schedule_id=-1,
            schedulelog_id=-1,
            success_count=0,
            failure_count=0,
            warning_count=0,
            total_count=0
        )
        job_run.save()

        try:

            reader = self.get_reader(job, source_config)
            reader.setup()
            if not reader.input_object:
                job_run.message = 'No input available to process'
                job_run.status = 'NoInput'
                job_run.sys_update_date = timezone.now()

            else:
                """
                    log job
                    fetch the filename and set it in log
                """
                job_run.filename = reader.input_object
                """
                    set the mapper for regular job
                """
                mapper = None
                if job.run_type != 'A':
                    mapper = self.get_mapper(dest_config)
                    mapper.setup()
                """
                    fetch the write connector
                """
                writer = self.get_writer(dest_config)
                writer.setup(reader.header)

                for record in reader.read():
                    """
                        get transformer to map the record
                        to destination
                    """
                    logging.debug('Processing Record: %s',
                                  str(job_run.total_count))
                    mapped_record = record
                    if mapper:
                        mapped_record, map_warning = mapper.map(record)
                    """
                        we are ignoring the map_warning for the time
                    """
                    writer.write(mapped_record, record)
                    job_run.total_count += 1

                """
                    cleanup
                """
                writer.down()
                if mapper:
                    mapper.down()
                reader.down()

                if writer.output_object and job_run.total_count > 0:
                    failure_count, warning_count = self.save_response(
                        job_run, writer.output_object)
                    job_run.failure_count = failure_count
                    job_run.warning_count = warning_count
                    job_run.success_count = job_run.total_count - job_run.failure_count

                job_run.message = 'processed'
                job_run.status = 'Complete'

        except SIDException as exp:
            job_run.status = 'Failure'
            job_run.message = str(exp)
        except Exception as exp:
            logging.error(str(exp))
            job_run.status = 'Failure'
            job_run.message = str(exp)

        job_run.sys_update_date = timezone.now()
        job_run.save()

        logging.debug('Job Run Finished')

        return job_run

    def get_reader(self, job, config):
        """
            get connector
        """
        if job.run_type == 'A':
            """
                if it's adhoc then we get the reader
                from JobHook
            """
            from apps.hook.jobhook import JobHook
            job_hook = JobHook()
            try:
                connector = job_hook.reader(self.user_id, self.run_date, job)
                return connector
            except Exception:
                SIDException('Invalid Adhoc connector')

        connector_name = config.conn_object.conn_name.conn_name.lower()
        connector = None
        if connector_name == 'salesforce':
            from core.connectors.salesforce.reader import Reader
        elif connector_name == 'file':
            from core.connectors.file.reader import Reader
        elif connector_name == 'aws_s3':
            from core.connectors.awss3.reader import Reader
        else:
            raise SIDException('Connector not supported')

        connector = Reader(
            user_id=self.user_id,
            run_date=self.run_date,
            config=config
        )

        return connector

    def get_writer(self, config):
        """
            get connector
        """
        connector_name = config.conn_object.conn_name.conn_name.lower()
        connector = None
        if connector_name == 'salesforce':
            from core.connectors.salesforce.writer import Writer
        elif connector_name == 'file':
            from core.connectors.file.writer import Writer
        elif connector_name == 'aws_s3':
            from core.connectors.awss3.writer import Writer
        else:
            raise SIDException('Connector not supported')

        connector = Writer(
            user_id=self.user_id,
            run_date=self.run_date,
            config=config
        )

        return connector

    def get_mapper(self, config):
        """
            get connector
        """
        connector_name = config.conn_object.conn_name.conn_name.lower()
        connector = None
        if connector_name == 'salesforce':
            from core.connectors.salesforce.mapper import Mapper
        elif connector_name == 'file' or connector_name == 'aws_s3':
            from core.connectors.file.mapper import Mapper
        # elif connector_name == 'AWS_S3':
        #     from core.connectors.awss3.mapper import Mapper
        else:
            raise SIDException('Connector not supported')

        connector = Mapper(
            user_id=self.user_id,
            run_date=self.run_date,
            config=config
        )

        return connector

    def get_jobconfig(self, job_id, adhoc_job=False):
        """
            fetch job config
        """
        from core.models.coreproxy import JobConfigProxy

        """
                Before we execute let's get config details
        """
        job_configs = JobConfigProxy.objects.filter(
            job_id=job_id
        )
        if adhoc_job:
            """
                we only expect destination connector
            """
            if len(job_configs) != 1 or job_configs[0].rec_type != 'D':
                raise SIDException('Invalid Adhoc Job Configuration', 'Dest')

            return (None, job_configs[0])

        if len(job_configs) != 2:
            raise SIDException('Invalid Job Configuration', 'Source / Dest')

        if job_configs[0].rec_type == 'S':
            source_config = job_configs[0]
        else:
            dest_config = job_configs[0]

        if job_configs[1].rec_type == 'D':
            dest_config = job_configs[1]
        else:
            source_config = job_configs[1]

        if not source_config or not dest_config:
            raise SIDException('Job Configuration Missing', 'Source / Dest')

        if source_config.conn_object.conn_name.conn_name == 'Salesforce' and\
                source_config.query:
            """
                if salesforce is source config
                then convert query
            """
            source_config.query = ast.literal_eval(source_config.query)

        logging.debug('Source and Destination configuration fetched')

        return (source_config, dest_config)

    def get_job(self):
        """
            get job details
        """
        from core.models.coreproxy import JobsProxy
        """
            check if the job is active
        """
        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        query = Q(Q(
            job__object_type='Job') & Q(job_id=self.job_id) & Q(
                Q(job__expiration_date__gte=datetime.today()) | Q(
                    job__expiration_date__isnull=True)
        )
        )
        if sid_settings.sidadmin != self.user_id:
            query = Q(Q(job__object_type='Job') & Q(
                job__object_owner=self.user_id) & Q(
                    job_id=self.job_id) & Q(Q(
                        job__expiration_date__gte=datetime.today()) | Q(
                            job__expiration_date__isnull=True)
            )
            )
        job_records = JobsProxy.objects.filter(
            query
        )
        if len(job_records) < 1:
            """
                job is not active
            """
            raise SIDException('No Active Job found', str(self.job_id))

        return job_records[0]

    def executebyfile(self,
                      download_path,
                      download_file,
                      delimiter,
                      lineterminator):
        """
            run the job
        """
        if not download_path or not download_file:
            """
                make sure user / job_name is populated
            """
            raise SIDException('Mandatory Field Missing', 'Input file missing')

        logging.debug('Starting Job: %s', str(self.job_id))
        job = self.get_job()
        """
                Before we execute let's get config details
        """
        source_config, dest_config = self.get_jobconfig(job.job_id)

        logging.debug('Source and Destination configuration fetched')
        source_config.delimiter = delimiter
        source_config.lineterminator = lineterminator
        """
            set the filename to local
        """
        source_config.conn_object.conn_name.conn_name = 'File'
        source_config.conn_object.name = 'SidLocal'
        source_config.filepath = download_path
        source_config.filestartwith = download_file
        source_config.fileendwith = None
        source_config.filemask = None

        return self.run_jobbyconfig(job, source_config, dest_config)

    def get_joblog(self,
                   job,
                   status,
                   filename=None):
        """
            create job log
        """
        from core.models.coreproxy import JobrunLogProxy

        job_run = JobrunLogProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            job=job,
            run_date=self.run_date,
            status='Running',
            filename=filename,
            schedule_id=self.schedule_id,
            schedulelog_id=self.schedulelog_id
        )
        job_run.save()
        return job_run

    def reprocess_failures(self, jobrun_id):
        """
            reprocess failed records
        """
        job = self.get_job()
        logging.debug('Processing Job: %s', job.job_name)
        """
            let's get user settings
        """
        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        if not sid_settings.settings:
            """
                user settings missing
            """
            raise SIDException('User settings missing')

        from core.models.coreproxy import JobrunDetailsProxy
        records = JobrunDetailsProxy.objects.filter(
            jobrun_id=jobrun_id,
            status_code='failure'
        )
        if len(records) < 1:
            """
                Invalid Job
            """
            logging.error('No failure records to process')
            return

        """
            we use the existing jobrun date
            records[0].jobrun.run_date
        """

        """
            fetch config
        """
        source_config, dest_config = self.get_jobconfig(job_id=job.job_id)

        writer = self.get_writer(dest_config)
        writer.setup(None)

        import ast
        for jobdetail in records:
            if jobdetail.processed_record:
                curr_record = ast.literal_eval(jobdetail.processed_record)
                writer.write(curr_record, curr_record)

        if writer:
            writer.down()

        from core.models.coreproxy import JobrunLogProxy
        """
                Let's run the job
        """
        job_run = JobrunLogProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            job=job,
            run_date=records[0].jobrun.run_date,
            status='Running',
            filename=None,
            schedule_id=-1,
            schedulelog_id=-1,
            success_count=0,
            failure_count=0,
            warning_count=0,
            total_count=len(records)
        )
        job_run.save()

        if writer.output_object:
            failure_count, warning_count = self.save_response(
                job_run, writer.output_object)
            job_run.failure_count = failure_count
            job_run.warning_count = warning_count
            job_run.success_count = len(records) - job_run.failure_count
        job_run.message = 'processed'
        job_run.status = 'Complete'
        job_run.save()

    def save_response(self, jobrun, responserecs):
        """
            save all the connector response
        """
        from core.models.coreproxy import JobrunDetailsProxy

        error_count = 0
        warning_count = 0
        for response in responserecs:
            status_code = response.get('status_code', None)
            if not status_code:
                continue

            job_details = JobrunDetailsProxy(
                sys_creation_date=timezone.now(),
                user_id=self.user_id,
                jobrun=jobrun,
                record_key=response.get('record_key', ''),
                record_value=response.get('field_value', ''),
                status_code=status_code,
                status_message=response.get('status_message', ''),
                orig_record=response.get('orig_record', ''),
                processed_record=response.get('processed_record', '')
            )
            job_details.save()
            if status_code == 'failure':
                error_count += 1
            else:
                warning_count += 1
        return [error_count, warning_count]
