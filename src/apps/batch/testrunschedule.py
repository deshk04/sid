import logging
from datetime import date, datetime
import argparse

from core.general.appinit import app_init
from core.general.exceptions import SIDException
from core.general import settings


def set_arguments():
    """
        set the command line arguments
    """

    parser = argparse.ArgumentParser(
        description='Script to Run Schedule, '
        'SID uses this script to run schedule jobs')

    # directories
    parser.add_argument(
        '--schedule_id', required=True,
        help='If you dont know schedule_id, please check the schedule table')  # noqa

    return parser.parse_args()


def get_arguments(args):
    """
        get the command line arguments
    """

    arguments = dict()
    arguments['schedule_id'] = args.schedule_id

    return arguments


def run():
    """
        run the scheduler
    """
    # set command line arguments
    args = set_arguments()

    # get the arguments
    arguments = get_arguments(args)

    # run_date = date(2020, 10 ,26)
    schedule_id = arguments['schedule_id']
    run_schedule(settings.SID_ADMIN, schedule_id)


def testrun():
    """
        run the scheduler
    """
    run_date = date(2021, 6, 8)
    schedule_id = 22
    run_schedule(
        settings.SID_ADMIN,
        schedule_id,
        'Y',
        run_date
    )


def run_schedule(user_id, schedule_id, rerun_flag='N', run_date=None):
    """
        test mapper
    """
    app_init()

    logging.debug('run schedule: %s', str(schedule_id))
    if not schedule_id:
        logging.debug('Invalid schedule_id')
        return

    """
        check the schedule object and schedule owner
    """
    if not user_id:
        from django.db.models import Q

        from core.models.coreproxy import ObjectProxy
        query = Q(
            Q(object_type='Schedule') & Q(
                schedule_id=str(schedule_id)) & Q(
                Q(schedule__expiration_date__gte=datetime.today()) | Q(
                    schedule__expiration_date__isnull=True)
            )
        )

        object_records = ObjectProxy.objects.filter(
            query
        )
        if not object_records:
            raise SIDException('Not valid scheduler')
        user_id = object_records[0].object_owner

    from core.controller.schedulecontroller import ScheduleController

    schedule_controller = ScheduleController(
        user_id=user_id,
        schedule_id=schedule_id
    )
    if run_date:
        schedule_controller.run_date = run_date
    try:
        schedule_controller.execute(rerun_flag)
    except SIDException as exp:
        logging.error('schedule failure for %s', str(schedule_id))


if __name__ == '__main__':
    """
        start
    """
    testrun()
