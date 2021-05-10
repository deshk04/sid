import os
from datetime import datetime

from django.http import HttpResponse
from django.db.models import Q, F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from sid.helper.apiresponse import ApiResponse


def fetchjoblogs(user_id, startdate, enddate):
    """
        job log details
    """

    from core.models.coreproxy import JobrunLogProxy

    """
        fetch all job logs
    """
    # query = Q(
    #     Q(job__job__object_owner=user_id) & Q(job__job__object_type='Job') &
    #     Q(Q(job__job__expiration_date__gte=datetime.today()) |
    #       Q(job__job__expiration_date__isnull=True)
    #       )
    # )
    """
        change the filter as per the dates
    """
    query = Q(Q(job__job__object_owner=user_id) & Q(
        job__job__object_type='Job') & Q(
            Q(job__job__expiration_date__gte=datetime.today()) | Q(
                job__job__expiration_date__isnull=True)
    ) & Q(
            Q(run_date__gte=startdate) & Q(run_date__lte=enddate)
    )
    )

    records = JobrunLogProxy.objects.filter(
        query
    ).values('id', 'job_id', 'job__job_name', 'job__run_type',
             'filename', 'file_date',
             'run_date', 'message', 'status',
             'success_count', 'failure_count', 'warning_count',
             'total_count',
             'sys_creation_date', 'sys_update_date').annotate(
        jobrun_id=F('id'),
        job_name=F('job__job_name'),
        run_type=F('job__run_type'),
        start_date=F('sys_creation_date'),
        end_date=F('sys_update_date')
    ).values(
                 'jobrun_id', 'job_id', 'job_name', 'run_type',
                 'filename', 'file_date',
                 'run_date', 'message', 'status',
                 'job_name', 'start_date', 'end_date',
                 'success_count', 'failure_count', 'warning_count',
                 'total_count'
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


def fetchjoblogbyid(user_id, jobrun_id):
    """
        job log details
    """

    from core.models.coreproxy import JobrunLogProxy

    """
        fetch all job logs
    """
    """
        change the filter as per the dates
    """
    query = Q(Q(job__job__object_owner=user_id) & Q(
        job__job__object_type='Job') & Q(
            Q(job__job__expiration_date__gte=datetime.today()) | Q(
                job__job__expiration_date__isnull=True)
    ) & Q(id=jobrun_id)
    )

    records = JobrunLogProxy.objects.filter(
        query
    ).values('id', 'job_id', 'job__job_name', 'job__run_type',
             'filename', 'file_date',
             'run_date', 'message', 'status',
             'success_count', 'failure_count', 'warning_count',
             'total_count',
             'sys_creation_date', 'sys_update_date').annotate(
        jobrun_id=F('id'),
        job_name=F('job__job_name'),
        run_type=F('job__run_type'),
        start_date=F('sys_creation_date'),
        end_date=F('sys_update_date')
    ).values(
                 'jobrun_id', 'job_id', 'job_name', 'run_type',
                 'filename', 'file_date',
                 'run_date', 'message', 'status',
                 'job_name', 'start_date', 'end_date',
                 'success_count', 'failure_count', 'warning_count',
                 'total_count'
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getjoblogs(request):
    """
        job log details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

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
        enddate = datetime.fromtimestamp(enddate / 1000.0)
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

    records['joblogs'] = fetchjoblogs(user_id, startdate, enddate)

    """
        let's get job logs
    """
    response_record.setrecords(records)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadlog(request):
    """
        job log download
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    # user_id = 'admin'

    from core.models.coreproxy import JobrunLogProxy

    jobrun_id = request.GET.get('jobrun_id', None)
    if not jobrun_id:
        response_record.status = 'error'
        response_record.message.append('Invalid Input')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

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
        response_record.status = 'error'
        response_record.message.append('Invalid Job')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    # response_record.setrecords(records)
    try:
        from core.controller.logcontroller import LogController
        log_controller = LogController(user_id=user_id)
        log_controller.job = records[0].job
        log_controller.jobrun = records[0]
        log_controller.execute()
        if not log_controller.log_file:
            response_record.status = 'error'
            response_record.message.append('Missing Log File')
            return HttpResponse(response_record.dumpoutput(),
                                content_type='application/javascript; charset=utf8'
                                )

    except Exception:
        response_record.status = 'error'
        response_record.message.append('Missing Log File')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    with open(log_controller.log_file, 'rb') as handle:
        response = HttpResponse(handle.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        content_text = 'attachment; filename=' + \
            os.path.basename(log_controller.log_file)
        response['Content-Disposition'] = content_text
        return response

    response_record.status = 'error'
    response_record.message.append('Missing Log File')
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def runfailedrecords(request):
    """
        job log download
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    # user_id = 'admin'

    from core.models.coreproxy import JobrunLogProxy

    jobrun_id = request.GET.get('jobrun_id', None)
    if not jobrun_id:
        response_record.status = 'error'
        response_record.message.append('Invalid Input')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

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
        response_record.status = 'error'
        response_record.message.append('Invalid Job')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    # response_record.setrecords(records)
    try:
        from core.controller.logcontroller import LogController
        log_controller = LogController(user_id=user_id)
        log_controller.job = records[0].job
        log_controller.jobrun = records[0]
        log_controller.execute()
        if not log_controller.log_file:
            response_record.status = 'error'
            response_record.message.append('Missing Log File')
            return HttpResponse(response_record.dumpoutput(),
                                content_type='application/javascript; charset=utf8'
                                )

    except Exception:
        response_record.status = 'error'
        response_record.message.append('Missing Log File')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    with open(log_controller.log_file, 'rb') as handle:
        response = HttpResponse(handle.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        content_text = 'attachment; filename=' + \
            os.path.basename(log_controller.log_file)
        response['Content-Disposition'] = content_text
        return response

    response_record.status = 'error'
    response_record.message.append('Missing Log File')
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getjoblogbyid(request):
    """
        job log details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    jobrun_id = request.GET.get('jobrun_id', None)

    if not jobrun_id:
        response_record.status = 'error'
        response_record.message.append('Invalid Input')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records['joblogs'] = fetchjoblogbyid(user_id, jobrun_id)

    """
        let's get job logs
    """
    response_record.setrecords(records)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
