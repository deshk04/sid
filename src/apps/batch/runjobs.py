import logging
from datetime import date

from core.general.appinit import app_init
from core.general.exceptions import SIDException


def run_jobs(user_id, job_id, run_date):
    """
        test run job
    """
    app_init()

    from core.controller.jobcontroller import JobController

    job_controller = JobController(
        user_id=user_id,
        job_id=job_id,
        run_date=run_date
    )
    rerun_flag = True
    try:
        job_controller.execute(
            -1, -1, rerun_flag
        )
    except SIDException as exp:
        logging.error('Job failure for %s', str(job_id))

    logging.debug('Job finished ')
    print('Complete')


if __name__ == '__main__':
    """
        start
    """
    user_id = 'admin'
    job_id = 18

    run_jobs(
        user_id,
        job_id,
        date(2021, 6, 3)
    )
