from django.utils import timezone
from django.db.models import Q
from datetime import datetime, date

from core.general.appinit import app_init
from core.general.exceptions import SIDException
from core.general import settings

import ast


def extract_csv():
    """
        main function
    """
    app_init()

    from core.models.coreproxy import JobrunLogProxy

    jobrun_id = 1223
    user_id = 'admin'

    query = Q(Q(job__job__object_owner=user_id) & Q(
        job__job__object_type='Job') & Q(
        Q(job__job__expiration_date__gte=datetime.today()) | Q(
            job__job__expiration_date__isnull=True)
    ) & Q(id=jobrun_id)
    )
    records = JobrunLogProxy.objects.filter(query)
    if len(records) < 1:
        """
            Invalid Job
        """
        print('Invalid job')
        return

    try:
        from core.controller.logcontroller import LogController
        log_controller = LogController(user_id=user_id)
        log_controller.job = records[0].job
        log_controller.jobrun = records[0]
        log_controller.execute('error')
        if not log_controller.log_file:
            print('Error producing logfile')
    except Exception:
        print('Exception in log controller')


def reprocess_failures(jobrun_id):
    """
        main function
    """
    app_init()

    from core.models.coreproxy import JobsProxy, JobConfigProxy

    jobrun_id = 1223
    job_id = 18
    user_id = 'admin'
    run_date = date(2020, 1, 1)

    query = Q(Q(job__object_type='Job') & (
        Q(job__object_owner=user_id) | Q(
            job__object_owner='admin')) & Q(job_id=job_id) & Q(
        Q(job__expiration_date__gte=datetime.today()) | Q(
            job__expiration_date__isnull=True)
    )
    )

    job_records = JobsProxy.objects.filter(
        query
    )
    if not job_records:
        """
            job is not active
        """
        raise SIDException('No Active Job found', str(job_id))

    job = job_records[0]
    job_configs = JobConfigProxy.objects.filter(
        job_id=job.job_id
    )
    if len(job_configs) != 2:
        raise SIDException('Invalid Job Configuration', 'Source / Dest')

    source_config = None
    dest_config = None
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

    from core.models.coreproxy import JobrunLogProxy
    jobrun = JobrunLogProxy()

    from core.controller.sfcontroller import SFController
    from core.connectors.file.reader import Reader

    sf_controller = SFController(
        user_id=user_id
    )
    sf_controller.reader = Reader()
    sf_controller.source_config = source_config
    sf_controller.dest_config = dest_config
    sf_controller.jobrun = jobrun
    sf_controller.parallel_count = 1
    try:
        sf_controller.execute_for_failed(jobrun_id)
    except SIDException as exp:
        raise SIDException('Error in execute for failed', '')


if __name__ == '__main__':
    """
        start
    """
    # extract_csv()
    reprocess_failures(1223)
