import asyncio
from asgiref.sync import sync_to_async
import json

from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.db.models import Q, F
from django.utils import timezone
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from sid.helper.apiresponse import ApiResponse
from core.general.exceptions import SIDException
from core.general.sidhelper import cleanfield


def fetchschedules(user_id):
    """
        schedule details
    """
    from core.models.coreproxy import ScheduleProxy

    """
        fetch all connector objects
    """
    query = Q(
        Q(schedule__object_owner=user_id) & Q(
            schedule__object_type='Schedule') & Q(
                Q(schedule__expiration_date__gte=datetime.today()) | Q(
                    schedule__expiration_date__isnull=True)
        )
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = ScheduleProxy.objects.filter(
        query
    ).values('schedule_id',
             'schedule_type', 'schedule_name',
             'frequency',
             'sys_creation_date',
             'sys_update_date').annotate(
        id=F('schedule_id'),
        create_date=F('sys_creation_date'),
        modified_date=F('sys_update_date')
    ).values(
                 'id', 'schedule_type',
                 'schedule_name', 'frequency',
                 'create_date', 'modified_date'
    )
    for record in records:
        if record['create_date']:
            record['create_date'] = record['create_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['modified_date']:
            record['modified_date'] = record['modified_date'].strftime(
                '%Y-%m-%d %H:%M:%S')

    result = list(records)

    return result


def fetchscheduleconfig(user_id):
    """
        connection details
    """
    from core.models.coreproxy import ScheduleConfigProxy

    """
        fetch all connector objects
    """
    query = Q(Q(schedule__schedule__object_owner=user_id) & Q(
        schedule__schedule__object_type='Schedule') & Q(
            Q(schedule__schedule__expiration_date__gte=datetime.today()
              ) | Q(schedule__schedule__expiration_date__isnull=True)
    )
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = ScheduleConfigProxy.objects.filter(
        query
    ).values('schedule_id', 'job_sequence', 'job__job_id',
             'job__job_name').annotate(
        id=F('schedule_id'),
        job_id=F('job__job_id'),
        job_name=F('job__job_name')
    ).values(
                 'id', 'job_sequence', 'job_id',
                 'job_name'
    )

    result = list(records)

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getschedules(request):
    """
        schedule details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    records['schedules'] = fetchschedules(user_id)
    records['scheduleconfig'] = fetchscheduleconfig(user_id)

    """
        let's get user's schedule
    """

    response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def markScheduleComplete(user_id, schedule_id, run_date, markascomplete):
    """
        execute schedule
    """
    response_record = ApiResponse()

    from core.controller.schedulecontroller import ScheduleController

    schedule_controller = ScheduleController(
        user_id=user_id
    )

    schedule_controller.run_date = run_date
    schedule_controller.mark_complete = markascomplete
    schedule_controller.schedule_id = schedule_id
    # schedule_controller.schedule_name = 'dummy'
    try:
        schedule_controller.execute('Y')
    except SIDException as exp:
        message = str(exp)
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    except Exception:
        message = 'Error running schedule'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record

    response_record.status = 'ok'

    if schedule_controller.schedule_log:
        message = schedule_controller.schedule_log.status + ' : ' +\
            schedule_controller.schedule_log.message
        if schedule_controller.schedule_log == 'Failed':
            response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    else:
        message = 'Error running schedule'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record


@sync_to_async
def executeSchedule(user_id, schedule_id, run_date, markascomplete):
    """
        execute schedule
    """
    response_record = ApiResponse()
    from core.general.sidhelper import setup_logfile
    setup_logfile()

    from core.controller.schedulecontroller import ScheduleController

    schedule_controller = ScheduleController(
        user_id=user_id
    )

    schedule_controller.run_date = run_date
    schedule_controller.mark_complete = markascomplete
    schedule_controller.schedule_id = schedule_id
    # schedule_controller.schedule_name = 'dummy'
    try:
        schedule_controller.execute('Y')
    except SIDException as exp:
        message = str(exp)
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    except Exception:
        message = 'Error running schedule'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record

    response_record.status = 'ok'

    if schedule_controller.schedule_log:
        message = schedule_controller.schedule_log.status + ' : ' +\
            schedule_controller.schedule_log.message
        if schedule_controller.schedule_log == 'Failed':
            response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    else:
        message = 'Error running schedule'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record


async def setexecutebyid(user_id, schedule_id, run_date, markascomplete):
    # asyncio.ensure_future(
    #     sync_to_async(executeSchedule(
    #         user_id, schedule_id, run_date, markascomplete)
    #         )
    # )
    asyncio.ensure_future(executeSchedule(
        user_id, schedule_id, run_date, markascomplete)
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def runschedule(request):
    """
        schedule run details
    """
    response_record = ApiResponse()
    # records = {}
    user_id = request.user.username

    schedule_id = request.GET.get('schedule_id', None)
    run_date = request.GET.get('rundate', None)
    markcomplete = request.GET.get('markcomplete', 'N')
    if markcomplete and markcomplete == 'Y':
        markcomplete = True
    else:
        markcomplete = False

    if not schedule_id:
        response_record.status = 'error'
        response_record.message.append('Input Schedule is missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    try:
        run_date = int(run_date)
        run_date = datetime.fromtimestamp(run_date / 1000.0)
        if run_date.year < 2020:
            run_date = None
    except Exception:
        run_date = None

    if not run_date:
        response_record.status = 'error'
        response_record.message.append('Run Date is missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    """
        let's get user's job details
    """
    # response_record = executeSchedule(
    #     user_id, schedule_id, run_date, markcomplete)
    if markcomplete:
        response_record = markScheduleComplete(
            user_id, schedule_id, run_date, markcomplete)
    else:
        asyncio.run(setexecutebyid(
            user_id, schedule_id, run_date, markcomplete))

        response_record.message.append(
            'Schedule run in background, Please check log for latest update')
        response_record.status = 'ok'

    # response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def fetchschjobrun(schedule_id, schedulelog_id):
    """
        fetch job run summary
    """
    from core.models.coreproxy import JobrunLogProxy

    """
        fetch all schedule jobrun logs
    """
    query = Q(Q(schedule_id=schedule_id) & Q(schedulelog_id=schedulelog_id))

    records = JobrunLogProxy.objects.filter(
        query
    ).values('id', 'job_id', 'run_date', 'message', 'status',
             'success_count', 'failure_count', 'warning_count',
             'total_count', 'job__job_name',
             'sys_creation_date', 'sys_update_date').annotate(
        jobrun_id=F('id'),
        job_name=F('job__job_name'),
        start_date=F('sys_creation_date'),
        end_date=F('sys_update_date')
    ).values(
        'jobrun_id', 'job_id', 'run_date', 'message',
        'status', 'success_count', 'failure_count', 'warning_count',
        'total_count', 'job_name',
        'start_date', 'end_date'
    )
    for record in records:
        if record['start_date']:
            record['start_date'] = record['start_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['end_date']:
            record['end_date'] = record['end_date'].strftime(
                '%Y-%m-%d %H:%M:%S')

    result = list(records)
    return result


def fetchschedulelogs(user_id, schedule_id, startdate, enddate):
    """
        schedule log details
    """
    from core.models.coreproxy import ScheduleLogProxy

    """
        fetch all schedule logs
    """
    # enddate = date.today()
    # startdate = enddate + timedelta(days=settings.LOG_DAYS)

    query = Q(Q(schedule__schedule__object_owner=user_id) & Q(
        schedule__schedule__object_type='Schedule') & Q(
            Q(schedule__schedule__expiration_date__gte=datetime.today()
              ) | Q(schedule__schedule__expiration_date__isnull=True)
    ) & Q(
            Q(run_date__gte=startdate) & Q(run_date__lte=enddate)
    )
    )

    records = ScheduleLogProxy.objects.filter(
        query
    ).values('id', 'schedule_id', 'run_date', 'message', 'status',
             'sys_creation_date', 'sys_update_date').annotate(
        schedulelog_id=F('id'),
        start_date=F('sys_creation_date'),
        end_date=F('sys_update_date')
    ).values(
        'schedulelog_id',
        'schedule_id', 'run_date', 'message',
        'status', 'start_date', 'end_date'
    )
    result = []
    for record in records:
        if record['start_date']:
            record['start_date'] = record['start_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['end_date']:
            record['end_date'] = record['end_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        """
            fetch the job run details
        """
        jobrun = fetchschjobrun(schedule_id, record['schedulelog_id'])
        if jobrun:
            record['jobrun'] = jobrun
            result.append(record)

    # result = list(records)

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getschedulelogs(request):
    """
        schedule log details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    schedule_id = request.GET.get('schedule_id', None)

    if not schedule_id:
        response_record.status = 'error'
        response_record.message.append('Invalid Input')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    startdate = request.GET.get('startdate', None)
    enddate = request.GET.get('enddate', None)

    try:
        startdate = int(startdate)
        startdate = datetime.fromtimestamp(startdate / 1000.0)
        if startdate.year < 2020:
            startdate = None
    except Exception:
        startdate = None

    try:
        enddate = int(enddate)
        """
            add 1 more day to endate as query should
            include the data for last date
        """
        enddate = datetime.fromtimestamp(enddate / 1000.0) + timedelta(days=+1)
        if enddate.year < 2020:
            enddate = None
        if startdate and enddate and enddate < startdate:
            enddate = startdate
    except Exception:
        enddate = None

    if not startdate or not enddate:
        response_record.status = 'error'
        response_record.message.append('Invalid Date')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records = fetchschedulelogs(user_id, schedule_id, startdate, enddate)

    """
        let's get schedule logs
    """
    response_record.setrecords(records)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def fetchschedulesbyid(user_id, schedule_id):
    """
        schedule details
    """
    from core.models.coreproxy import ScheduleProxy

    """
        fetch all connector objects
    """
    query = Q(Q(schedule__object_owner=user_id) & Q(
        schedule__object_type='Schedule') & Q(
            schedule_id=schedule_id) & Q(
                Q(schedule__expiration_date__gte=datetime.today()
                  ) | Q(schedule__expiration_date__isnull=True)
    )
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = ScheduleProxy.objects.filter(
        query
    ).values('schedule_id',
             'schedule_type', 'schedule_name',
             'frequency', 'day_of_week', 'day_of_month',
             'hours', 'minutes',
             'sys_creation_date',
             'sys_update_date').annotate(
        id=F('schedule_id'),
        create_date=F('sys_creation_date'),
        modified_date=F('sys_update_date')
    ).values(
                 'id', 'schedule_type',
                 'schedule_name', 'frequency',
                 'day_of_week', 'day_of_month',
                 'hours', 'minutes',
                 'create_date', 'modified_date'
    )
    for record in records:
        if record['create_date']:
            record['create_date'] = record['create_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['modified_date']:
            record['modified_date'] = record['modified_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if not record['frequency']:
            record['frequency'] = 'Daily'
        if not record['day_of_week']:
            record['day_of_week'] = '0,1,2,3,4,5'
        if record['frequency'] == 'Monthly' and not record['day_of_month']:
            record['day_of_month'] = '1'
    if records:
        return records[0]
    else:
        return None


def fetchscheduleconfigbyid(user_id, schedule_id):
    """
        connection details
    """
    from core.models.coreproxy import ScheduleConfigProxy

    """
        fetch all connector objects
    """
    query = Q(Q(schedule__schedule__object_owner=user_id) & Q(
        schedule__schedule__object_type='Schedule') & Q(
            schedule__schedule_id=schedule_id) & Q(
                Q(schedule__schedule__expiration_date__gte=datetime.today()
                  ) | Q(schedule__schedule__expiration_date__isnull=True)
    )
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = ScheduleConfigProxy.objects.filter(
        query
    ).values('schedule_id', 'job_sequence', 'job__job_id',
             'job__job_name', 'job__run_type').annotate(
        id=F('schedule_id'),
        job_id=F('job__job_id'),
        job_name=F('job__job_name'),
        run_type=F('job__run_type')
    ).values(
                 'id', 'job_sequence', 'job_id',
                 'job_name', 'run_type'
    )

    result = list(records)

    return result


def fetchscheduledistbyid(user_id, schedule_id):
    """
        schedule details
    """
    from core.models.coreproxy import ScheduleDistributionProxy

    """
        fetch all connector objects
    """
    query = Q(Q(schedule__schedule__object_owner=user_id) & Q(
        schedule__schedule__object_type='Schedule') & Q(
            schedule__schedule_id=schedule_id) & Q(
                Q(schedule__schedule__expiration_date__gte=datetime.today()
                  ) | Q(schedule__schedule__expiration_date__isnull=True)
    )
    )

    records = ScheduleDistributionProxy.objects.filter(
        query
    ).values('schedule_id',
             'email_flag', 'tolist',
             'cclist',
             'bcclist').annotate(
        id=F('schedule_id')
    ).values(
                 'id', 'email_flag',
                 'tolist', 'cclist',
                 'bcclist'
    )
    # for record in records:
    #     if record['create_date']:
    #         record['create_date'] = record['create_date'].strftime(
    #             '%Y-%m-%d %H:%M:%S')
    #     if record['modified_date']:
    #         record['modified_date'] = record['modified_date'].strftime(
    #             '%Y-%m-%d %H:%M:%S')

    result = records[0]
    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getschedulebyid(request):
    """
        schedule details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    schedule_id = request.GET.get('schedule_id', None)
    if not schedule_id:
        response_record.status = 'error'
        response_record.message.append('Input Schedule id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    schedule = fetchschedulesbyid(user_id, schedule_id)
    if not schedule:
        response_record.status = 'error'
        response_record.message.append('Schedule details not found')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records['schedules'] = schedule
    records['scheduleconfig'] = fetchscheduleconfigbyid(user_id, schedule_id)
    records['distribution'] = fetchscheduledistbyid(user_id, schedule_id)

    """
        let's get user's schedule
    """
    response_record.setrecords(records)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateschedule(request):
    """
        new or update schedule
    """
    response_record = ApiResponse()
    user_id = request.user.username
    response_record.status = 'ok'

    if request.POST and request.POST.get('data', None):
        body = json.loads(request.POST['data'])
    else:
        """
            Error
        """
        response_record.status = 'error'
        response_record.message.append('Input data is missing or corrupt')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    schedules = body.get('schedules', None)
    if not schedules:
        response_record.status = 'error'
        response_record.message.append('schedule details missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    scheduleconfig = body.get('scheduleconfig', [])
    if not scheduleconfig:
        response_record.status = 'error'
        response_record.message.append('schedule steps missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    distribution = body.get('distribution', None)

    """
        validate and update
    """

    try:
        with transaction.atomic():
            return_val = check_schedule(user_id, schedules)
            if return_val[0]:
                response_record.status = 'error'
                response_record.message.append(return_val[0])
                raise

            schedule_record = return_val[1]
            if not schedule_record:
                response_record.status = 'error'
                response_record.message.append('Error creating schedule')
                raise

            return_val = check_config(user_id, schedule_record, scheduleconfig)
            if return_val[0]:
                response_record.status = 'error'
                response_record.message.append(return_val[0])
                raise

            schedule_config = return_val[1]
            if not schedule_config:
                response_record.status = 'error'
                response_record.message.append('Error creating schedule steps')
                raise

            return_val = check_distribution(
                user_id, schedule_record, distribution)
            if return_val[0]:
                response_record.status = 'error'
                response_record.message.append(return_val[0])
                raise

            schedule_dist = return_val[1]
            if not schedule_dist:
                response_record.status = 'error'
                response_record.message.append(
                    'Error creating schedule distribution')
                raise

    except Exception:
        transaction.rollback()
        response_record.status = 'error'
        response_record.message.append('Error updating job')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    response_record.status = 'ok'
    records = {}
    schedule = fetchschedulesbyid(user_id, schedule_record.schedule_id)
    if not schedule:
        response_record.status = 'error'
        response_record.message.append('Schedule details not found')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records['schedules'] = schedule
    records['scheduleconfig'] = fetchscheduleconfigbyid(
        user_id, schedule_record.schedule_id)
    records['distribution'] = fetchscheduledistbyid(
        user_id, schedule_record.schedule_id)
    response_record.setrecords(records)
    response_record.message.append('Schedule Details updated')
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8')


def check_schedule(user_id, schedules):
    """
        validate schedule
    """
    message = []

    schedule_id = schedules.get('id', None)
    schedule_name = cleanfield(schedules.get('schedule_name', None))
    schedule_type = cleanfield(schedules.get('schedule_type', 'R'))
    frequency = cleanfield(schedules.get('frequency', None))
    day_of_week = cleanfield(schedules.get('day_of_week', None))
    month = cleanfield(schedules.get('month', None))
    day_of_month = cleanfield(schedules.get('day_of_month', None))
    hours = cleanfield(schedules.get('hours', None))
    minutes = cleanfield(schedules.get('minutes', None))

    newschedule_flag = False
    if not schedule_id or schedule_id < 1:
        newschedule_flag = True

    try:
        schedule_id = int(schedule_id)
    except Exception:
        message.append('Invalid schedule Id')
        return [message, None]

    if not schedule_name or schedule_name.lower() == 'new' or schedule_name == '':
        message.append('Invalid schedule Name')
        return [message, None]

    if not frequency or frequency.lower() not in ['daily', 'monthly']:
        message.append('Invalid schedule frequency')
        return [message, None]

    if frequency.lower() == 'daily':
        if not day_of_week or day_of_week == '':
            message.append('Invalid schedule daily frequency')
            return [message, None]
        day_of_week = day_of_week.split(',')
        if not day_of_week:
            message.append('Invalid schedule daily frequency')
            return [message, None]
        day_of_week = ','.join(day_of_week)

    if frequency.lower() == 'monthly':
        if not day_of_month or day_of_month == '':
            message.append('Invalid schedule monthly frequency')
            return [message, None]
        try:
            day_of_month = int(day_of_month)
        except Exception:
            message.append('Invalid schedule monthly frequency')
            return [message, None]
    if not hours or not minutes:
        message.append('Invalid schedule frequency time')
        return [message, None]
        try:
            hours = int(hours)
        except Exception:
            message.append('Invalid schedule frequency hours')
            return [message, None]
        if not minutes:
            minutes = 0

    from core.models.coreproxy import ScheduleProxy, ObjectProxy
    schedule_record = None
    if newschedule_flag:
        """
            make sure schedule_name is different
        """
        query = Q(Q(schedule__object_owner=user_id) & Q(
            schedule__object_type='Schedule') & Q(schedule_name=schedule_name)
        )
        schedule_records = ScheduleProxy.objects.filter(
            query
        )
        if schedule_records:
            message.append('Error: Schedule already exists')
            return [message, None]

        object_record = ObjectProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            object_type='Schedule',
            object_key=schedule_name,
            object_owner=user_id,
            effective_date=timezone.now(),
            expiration_date=date(4999, 12, 31)
        )
        object_record.save()

        schedule_record = ScheduleProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            schedule=object_record,
            schedule_name=schedule_name,
            schedule_type=schedule_type,
            schedule_owner=user_id,
            frequency=frequency,
            day_of_week=day_of_week,
            month=month,
            day_of_month=day_of_month,
            hours=hours,
            minutes=minutes
        )

    else:
        query = Q(
            Q(schedule__object_owner=user_id) & Q(
                schedule__object_type='Schedule') & Q(
                    schedule__object_id=schedule_id)
        )
        schedule_records = ScheduleProxy.objects.filter(
            query
        )
        if schedule_records:
            schedule_record = schedule_records[0]
            schedule_record.sys_update_date = timezone.now()
            schedule_record.user_id = user_id
            schedule_record.schedule_name = schedule_name
            schedule_record.schedule_type = schedule_type
            schedule_record.schedule_owner = user_id
            schedule_record.frequency = frequency
            schedule_record.day_of_week = day_of_week
            schedule_record.month = month
            schedule_record.day_of_month = day_of_month
            schedule_record.hours = hours
            schedule_record.minutes = minutes

        else:
            message.append('Schedule not found')

    if message:
        return [message, None]

    schedule_record.save()

    return [message, schedule_record]


def check_config(user_id, schedule, schedule_configs):
    """
        check and update schedule config
    """
    message = []
    sch_configs = []
    from core.models.coreproxy import ScheduleConfigProxy, JobsProxy
    """
        remove existing records
    """
    ScheduleConfigProxy.objects.filter(
        schedule_id=schedule.schedule_id
    ).delete()
    for idx, config in enumerate(schedule_configs):
        job_sequence = config.get('job_sequence', None)
        job_id = config.get('job_id', None)
        if not job_sequence or not job_id:
            message.append('Error: Schedule step / job error')
            return [message, None]

        query = Q(Q(job__object_owner=user_id) & Q(
            job__object_type='Job') & Q(
                Q(job__expiration_date__gte=datetime.today()
                  ) | Q(job__expiration_date__isnull=True)
        ) & Q(job_id=job_id)
        )
        job_records = JobsProxy.objects.filter(
            query
        )
        if not job_records:
            message.append('Error: Schedule step, invalid job: ' + str(job_id))
            return [message, None]
        sch_config = ScheduleConfigProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            schedule=schedule,
            job_sequence=job_sequence,
            job_id=job_id
        )
        sch_config.save()
        sch_configs.append(sch_config)

    return [None, sch_configs]


def check_distribution(user_id, schedule, schedule_dist):
    """
        schedule distribution
    """
    message = []
    from core.models.coreproxy import ScheduleDistributionProxy

    schdist = None
    tolist = schedule_dist.get('tolist', None)
    if not tolist:
        """
            we remove the existing list
        """
        ScheduleDistributionProxy.objects.filter(
            schedule=schedule
        ).delete()
        return [message, 'Y']
    else:
        from django.core.validators import validate_email
        dist_list = []
        for mail in tolist.split(','):
            if not mail or len(mail) < 4:
                continue
            mail = mail.strip()
            try:
                validate_email(mail)
                dist_list.append(mail)
            except Exception:
                message.append('Invalid email address' + str(mail))
                return [message, None]
        tolist = ','.join(dist_list)
        if tolist:
            schdist = ScheduleDistributionProxy.objects.get_or_none(
                schedule=schedule
            )
            if schdist:
                schdist.sys_update_date = timezone.now()
                schdist.user_id = user_id
                schdist.email_flag = 'Y'
                schdist.tolist = tolist
            else:
                schdist = ScheduleDistributionProxy(
                    sys_creation_date=timezone.now(),
                    user_id=user_id,
                    schedule=schedule,
                    email_flag='Y',
                    tolist=tolist
                )
            schdist.save()

        return [message, schdist]
