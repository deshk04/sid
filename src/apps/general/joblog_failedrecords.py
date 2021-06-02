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


def reprocess_failures(job_id, jobrun_id):
    """
        main function
    """
    app_init()

    from core.controller.jobcontroller import JobController

    user_id = 'admin'
    run_date = date(2020, 1, 1)

    job_controller = JobController(
        user_id=user_id,
        job_id=job_id,
        run_date=run_date
    )
    job_controller.reprocess_failures(jobrun_id)

if __name__ == '__main__':
    """
        start
    """
    # extract_csv()
    reprocess_failures(18, 1223)
