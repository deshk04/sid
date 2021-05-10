import os
import asyncio
from asgiref.sync import sync_to_async

from datetime import datetime, date
import json
import ast
from django.http import HttpResponse
from django.db.models import Q, F
from django.utils import timezone
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.general.exceptions import SIDException
from core.general.sidhelper import cleanfield
from sid.helper.apiresponse import ApiResponse
from core.general import settings


def fetchjobfields(conn_id, model_name):
    """
        job field details
    """
    from core.models.coreproxy import FieldsProxy

    """
        fetch all job map objects
    """
    records = FieldsProxy.objects.filter(
        model__name=model_name,
        model__conn_object_id=conn_id
    ).values('model__name', 'field_name', 'field_type',
             'field_length',
             'field_format', 'label', 'primary_key'
             ).annotate(
        model_name=F('model__name')
    ).values(
        'model_name', 'field_name', 'field_type',
        'field_length',
        'field_format', 'label', 'primary_key').order_by('field_name')

    result = list(records)
    return result


def fetchjobmap(job_id):
    """
        job map details
    """
    from core.models.coreproxy import ModelMapProxy

    """
        fetch all job map objects
    """

    records = ModelMapProxy.objects.filter(
        job_id=job_id
    ).values('source_model', 'source_field', 'map_type',
             'map_value',
             'lookup_model', 'lookup_join_field', 'lookup_return_field',
             'dest_model', 'dest_field'
             )
    result = list(records)
    return result


def fetchjobconfig(job_id):
    """
        config details
    """
    from core.models.coreproxy import JobConfigProxy

    """
        fetch all config objects
    """
    records = JobConfigProxy.objects.filter(
        job_id=job_id
    ).values('job_id', 'rec_type', 'conn_object_id',
             'conn_object__name',
             'conn_object__conn_name',
             'conn_object__conn_system_type',
             'conn_object__conn_name__conn_logo_path',
             'filepath', 'filestartwith', 'fileendwith',
             'filemask', 'delimiter', 'encoding',
             'lineterminator', 'archivepath', 'key_field',
             'bulk_count', 'query', 'transaction_type', 'model'
             ).annotate(
        conn_id=F('conn_object_id'),
        conn_type=F('conn_object__conn_name'),
        conn_name=F('conn_object__name'),
        conn_system_type=F('conn_object__conn_system_type'),
        conn_logo_path=F('conn_object__conn_name__conn_logo_path')
    ).values(
        'job_id', 'rec_type', 'conn_id', 'conn_type',
        'conn_name', 'conn_system_type', 'conn_logo_path',
        'filepath', 'filestartwith', 'fileendwith',
        'filemask', 'delimiter', 'encoding',
        'lineterminator', 'archivepath', 'key_field',
        'bulk_count', 'query', 'transaction_type', 'model'
    )
    for record in records:
        if record['key_field'] and not record['transaction_type']:
            record['transaction_type'] = 'upsert'
        elif not record['transaction_type']:
            record['transaction_type'] = 'insert'
        if record['query'] and record['conn_type'] == 'Salesforce'\
                and len(record['query']) > 1:
            """
                if query
                then we need it to be in dict format
            """
            record['query'] = ast.literal_eval(record['query'])

    result = list(records)
    return result


def fetchjobs(user_id):
    """
        schedule details
    """
    from core.models.coreproxy import JobsProxy

    """
        fetch all connector objects
    """
    query = Q(Q(job__object_owner=user_id) & Q(
        job__object_type='Job') & Q(
            Q(job__expiration_date__gte=datetime.today()) | Q(
                job__expiration_date__isnull=True)
    )
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = JobsProxy.objects.filter(
        query
    ).values('job_id',
             'job_name',
             'run_type',
             'parallel_count',
             'sys_creation_date',
             'sys_update_date',
             'jobdistribution__tolist'
             ).annotate(
        create_date=F('sys_creation_date'),
        modified_date=F('sys_update_date'),
        tolist=F('jobdistribution__tolist')
    ).values(
                 'job_id', 'job_name',
                 'run_type', 'parallel_count',
                 'create_date', 'modified_date',
                 'tolist'
    )

    for record in records:
        if record['create_date']:
            record['create_date'] = record['create_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['modified_date']:
            record['modified_date'] = record['modified_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        # record['config'] = fetchjobconfig(record['job_id'])
        configs = fetchjobconfig(record['job_id'])

        for config in configs:
            if config['rec_type'] == 'S':
                record['source_config'] = config
            else:
                record['dest_config'] = config

    result = list(records)

    return result


def fetchconnectormodels(conn_id):
    """
        salesforce connector details
    """
    from core.models.coreproxy import DmodelsProxy
    """
        fetch all connector objects
    """
    query = Q(Q(conn_object_id=conn_id) & Q(name__isnull=False))
    model_records = DmodelsProxy.objects.filter(
        query).values('name', 'label').order_by('name')

    result = list(model_records)

    return result


def fetchjobbyid(user_id, job_id):
    """
        schedule details
    """
    from core.models.coreproxy import JobsProxy

    """
        fetch all connector objects
    """
    query = Q(Q(job__object_owner=user_id) & Q(job__object_type='Job') & Q(
        Q(job__expiration_date__gte=datetime.today()) | Q(
            job__expiration_date__isnull=True)
    ) & Q(job_id=job_id)
    )
    # conn_records = ConnectorProxy.objects.filter(query)

    records = JobsProxy.objects.filter(
        query
    ).values('job_id',
             'job_name',
             'run_type',
             'parallel_count',
             'sys_creation_date',
             'sys_update_date',
             'jobdistribution__tolist'
             ).annotate(
        create_date=F('sys_creation_date'),
        modified_date=F('sys_update_date'),
        tolist=F('jobdistribution__tolist')
    ).values(
                 'job_id', 'job_name',
                 'run_type', 'parallel_count',
                 'create_date', 'modified_date',
                 'tolist'
    )

    for record in records:
        if record['create_date']:
            record['create_date'] = record['create_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        if record['modified_date']:
            record['modified_date'] = record['modified_date'].strftime(
                '%Y-%m-%d %H:%M:%S')
        configs = fetchjobconfig(record['job_id'])

        source_conn_id = None
        dest_conn_id = None
        for config in configs:
            if config['rec_type'] == 'S':
                source_conn_id = config['conn_id']
                record['source_config'] = config
            else:
                dest_conn_id = config['conn_id']
                record['dest_config'] = config

        if record['run_type'] == 'R':
            record['map'] = fetchjobmap(record['job_id'])
            smodel_name = record['source_config']['model']
            record['sourcefields'] = fetchjobfields(
                source_conn_id, smodel_name)
            dmodel_name = record['dest_config']['model']
            record['destfields'] = fetchjobfields(dest_conn_id, dmodel_name)
        else:
            dmodel_name = record['dest_config']['model']
            record['destfields'] = fetchjobfields(dest_conn_id, dmodel_name)
            record['map'] = []

        record['models'] = fetchconnectormodels(dest_conn_id)
        if record.get('models', None) and not record.get('sourcefields', None):
            """
                for manual job setup we might not have source fields
                populated in dmodel / fields
                so we pick them up from map
            """
            fields = []
            for rec in record['map']:
                field = {
                    'model_name': '',
                    'field_name': '',
                    'field_type': 'Auto'
                }
                field['model_name'] = smodel_name
                field['field_name'] = rec['source_field']
                fields.append(field)
            record['sourcefields'] = fields

    result = list(records)

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getjobs(request):
    """
        schedule details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    # user_id = 'admin'
    records['jobs'] = fetchjobs(user_id)

    """
        let's get user's schedule
    """

    response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getjobbyid(request):
    """
        schedule details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    job_id = request.GET.get('job_id', None)
    if not job_id:
        response_record.status = 'error'
        response_record.message.append('Input Job id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    """
        let's get user's job details
    """
    records['jobs'] = fetchjobbyid(user_id, job_id)

    response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@sync_to_async
def executejobbyid(user_id, job_id, run_date):
    """
        execute job
    """
    response_record = ApiResponse()
    # records = {}
    from core.controller.schedulecontroller import run_job
    from core.general.sidhelper import setup_logfile

    setup_logfile()

    return_status = None
    try:
        return_status = run_job(
            job_id=job_id,
            run_date=run_date,
            user_id=user_id,
            rerun_flag='Y',
            schedule_id=-1,
            schedulelog_id=-1,
            mark_complete=False
        )
    except SIDException as exp:
        message = str(exp)
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    except Exception as exp:
        message = 'Error running job'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record

    """
        job was executed without any exception
    """
    job_name = str(return_status[0])
    jobrun_rec = return_status[2]
    if jobrun_rec:
        job_name = str(jobrun_rec.job_name)
    if return_status[1] == 0:
        response_record.status = 'error'
        message = 'Job failed: ' + job_name + ' please check the log'
        response_record.message.append(message)
    elif return_status[1] == 2:
        response_record.status = 'error'
        message = 'Input Source not available'
        response_record.message.append(message)
    else:
        response_record.status = 'ok'
        message = 'Success: Please check the log for more details'
        response_record.message.append(message)

    return response_record


async def setexecutejobbyid(user_id, job_id, run_date):
    asyncio.ensure_future(executejobbyid(user_id, job_id, run_date))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def runjobbyid(request):
    """
        job run details
    """
    response_record = ApiResponse()
    # records = {}
    user_id = request.user.username

    # user_id = 'admin'
    run_date = request.GET.get('rundate', None)
    job_id = request.GET.get('job_id', None)
    if not job_id:
        response_record.status = 'error'
        response_record.message.append('Input Job id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    try:
        run_date = int(run_date)
        run_date = datetime.fromtimestamp(run_date / 1000.0)
        if run_date.year < 2020:
            run_date = None
        run_date = run_date.date()
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
    asyncio.run(setexecutejobbyid(user_id, job_id, run_date))

    # response_record.setrecords(records)
    response_record.message.append(
        'Job run in background, Please check log for latest update')
    response_record.status = 'ok'
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def getsfobjects(user_id, conn_id, model_name):
    """
        refresh sf objects
    """
    response_record = ApiResponse()
    records = {}
    response_record.status = 'ok'

    from core.services.salesforce import SalesforceService

    sfservice = SalesforceService()
    try:
        sfservice.user_id = user_id
        sfservice.conn_id = conn_id
        sfservice.setup()
        records['models'] = sfservice.getmodels()
        records['fields'] = []
        if model_name:
            records['fields'] = fetchjobfields(conn_id, model_name)
        response_record.records = records

    except SIDException as exp:
        response_record.status = 'error'
        response_record.message.append(str(exp))

    return response_record


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getconnmodels(request):
    """
        refresh SF models
    """
    response_record = ApiResponse()
    user_id = request.user.username
    # user_id = 'admin'

    conn_id = request.GET.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Input connector missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    model_name = request.GET.get('model_name', None)

    """
        we have to call salesforce service to refresh model
    """
    response_record = getsfobjects(user_id, conn_id, model_name)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchconnmodels(request):
    """
        fetch connector model
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    # user_id = 'admin'

    conn_id = request.GET.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Input connector missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    model_name = request.GET.get('model_name', None)

    from core.models.coreproxy import ConnectorProxy

    """
        fetch connector object
    """
    query = Q(Q(object__object_owner=user_id) & Q(
        object__object_type='Connector') & Q(
            Q(object__expiration_date__gte=datetime.today()) | Q(
                object__expiration_date__isnull=True)
    ) & Q(object_id=conn_id)
    )
    conn_records = ConnectorProxy.objects.filter(query)

    if len(conn_records) < 1:
        response_record.status = 'error'
        response_record.message.append('Connector not found')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records['models'] = fetchconnectormodels(conn_id)

    if not model_name:
        """
            fetch models
        """
        records['fields'] = []
    else:
        """
            fetch fields
        """
        records['fields'] = fetchjobfields(conn_id, model_name)

    response_record.records = records

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatejob(request):
    """
        new or update job
    """
    response_record = ApiResponse()
    # records = {}
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

    """
        validation
    """
    try:
        with transaction.atomic():
            return_val = validate_job(user_id, body)
            if return_val[0]:
                response_record.status = 'error'
                response_record.message.append(return_val[0])
                raise

            job_record = return_val[1]
            if not job_record:
                response_record.status = 'error'
                response_record.message.append('Error creating job')
                raise

            if job_record.run_type == 'R':

                source_config = body.get('source_config', [])
                if not source_config:
                    response_record.status = 'error'
                    response_record.message.append('Invalid source')
                    raise

                return_val = validate_config(
                    user_id, job_record, source_config, 'S')
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                source_config = return_val[1]
                return_val = validate_model(
                    user_id,
                    source_config.conn_object,
                    source_config.model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise
                source_model = return_val[1]

                destconfig = body.get('dest_config', [])
                if not destconfig:
                    response_record.status = 'error'
                    response_record.message.append('Invalid destination')
                    raise

                return_val = validate_config(
                    user_id, job_record, destconfig, 'D')
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                dest_config = return_val[1]

                return_val = validate_model(
                    user_id,
                    dest_config.conn_object,
                    dest_config.model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                dest_model = return_val[1]

                mapdetails = body.get('map', [])
                return_val = validate_map(
                    user_id, source_config, dest_config, mapdetails)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                # map_configs = return_val[1]

                sourcefields = body.get('sourcefields', [])
                return_val = validate_fields(
                    user_id,
                    source_config,
                    sourcefields,
                    source_model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                destfields = body.get('destfields', [])
                return_val = validate_fields(
                    user_id,
                    dest_config,
                    destfields,
                    dest_model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

            else:
                destconfig = body.get('dest_config', [])
                if not destconfig:
                    response_record.status = 'error'
                    response_record.message.append('Invalid destination')
                    raise

                return_val = validate_config(
                    user_id, job_record, destconfig, 'D')
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

                dest_config = return_val[1]

                return_val = validate_model(
                    user_id,
                    dest_config.conn_object,
                    dest_config.model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise
                dest_model = return_val[1]

                destfields = body.get('destfields', [])
                return_val = validate_fields(
                    user_id,
                    dest_config,
                    destfields,
                    dest_model)
                if return_val[0]:
                    response_record.status = 'error'
                    response_record.message.append(return_val[0])
                    raise

    except Exception:
        transaction.rollback()
        response_record.status = 'error'
        response_record.message.append('Error updating job')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    response_record.status = 'ok'
    response_record.message.append('Job Details updated')
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8')


def validate_job(user_id, body):
    """
        validate job
    """
    message = []

    job_id = body.get('job_id', None)
    job_name = cleanfield(body.get('job_name', None))
    run_type = cleanfield(body.get('run_type', None))
    parallel_count = body.get('parallel_count', None)
    # create_date = cleanfield(body.get('create_date', None))
    # modified_date = cleanfield(body.get('modified_date', None))
    tolist = cleanfield(body.get('tolist', None))

    newjob_flag = False
    if not job_id or job_id < 1:
        newjob_flag = True

    try:
        job_id = int(job_id)
    except Exception:
        message.append('Invalid job Id')
        return [message, None]

    if not job_name or job_name.lower() == 'new' or job_name.strip() == '':
        message.append('Invalid job Name')
        return [message, None]

    if not run_type or run_type not in ['A', 'R']:
        message.append('Invalid job type')
        return [message, None]

    try:
        int(parallel_count)
    except Exception:
        parallel_count = 1
    dist_list = []
    if tolist:
        from django.core.validators import validate_email
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
    from core.models.coreproxy import JobsProxy, ObjectProxy, JobDistributionProxy

    job_record = None
    if newjob_flag:
        """
            make sure job_name is different
        """

        query = Q(Q(job__object_owner=user_id) & Q(
            job__object_type='Job') & Q(job_name=job_name)
        )
        job_records = JobsProxy.objects.filter(
            query
        )
        if job_records:
            message.append('Error: Job already exists')
            return [message, None]

        object_record = ObjectProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            object_type='Job',
            object_key=job_name,
            object_owner=user_id,
            effective_date=timezone.now(),
            expiration_date=date(4999, 12, 31)
        )
        object_record.save()

        job_record = JobsProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            job=object_record,
            job_name=job_name,
            run_type=run_type,
            parallel_count=parallel_count
        )
    else:

        query = Q(Q(job__object_owner=user_id) & Q(
            job__object_type='Job') & Q(job__object_id=job_id)
        )
        job_records = JobsProxy.objects.filter(
            query
        )
        if job_records:
            job_record = job_records[0]
            job_record.sys_update_date = timezone.now()
            job_record.user_id = user_id
            job_record.job_name = job_name
            job_record.run_type = run_type
            job_record.parallel_count = parallel_count

        else:
            message.append('Job not found')

    if message:
        return [message, None]

    job_record.save()
    """
        job distribution
    """
    if tolist:
        job_dist = JobDistributionProxy.objects.get_or_none(
            job_id=job_record.job_id
        )
        if job_dist:
            job_dist.sys_update_date = timezone.now()
            job_dist.user_id = user_id
            job_dist.email_flag = 'Y'
            job_dist.tolist = tolist
        else:
            job_dist = JobDistributionProxy(
                sys_creation_date=timezone.now(),
                user_id=user_id,
                job=job_record,
                email_flag='Y',
                tolist=tolist
            )
        job_dist.save()

    return [message, job_record]


def validate_config(user_id, job_record, config, config_type):
    """
        validate config
    """
    message = []

    conn_id = config.get('conn_id', None)
    conn_type = cleanfield(config.get('conn_type', None))
    conn_name = cleanfield(config.get('conn_name', None))
    # conn_system_type = cleanfield(config.get('conn_system_type', None))
    # conn_logo_path = cleanfield(config.get('conn_logo_path', None))
    filepath = cleanfield(config.get('filepath', None))
    filestartwith = cleanfield(config.get('filestartwith', None))
    fileendwith = cleanfield(config.get('fileendwith', None))
    filemask = cleanfield(config.get('filemask', None))
    delimiter = cleanfield(config.get('delimiter', None))
    encoding = cleanfield(config.get('encoding', None))
    lineterminator = cleanfield(config.get('lineterminator', None))
    archivepath = cleanfield(config.get('archivepath', None))
    key_field = cleanfield(config.get('key_field', None))
    bulk_count = config.get('bulk_count', None)
    query = config.get('query', None)
    transaction_type = cleanfield(config.get('transaction_type', None))
    model = cleanfield(config.get('model', None))

    if config_type == 'S':
        if not conn_id or not conn_name or not conn_type:
            message.append('Invalid Source Connector')
        else:
            if conn_type in ['File', 'AWS_S3']:
                if not filestartwith or not fileendwith:
                    message.append('Invalid Source File name')
                if not filepath:
                    message.append('Invalid Source File Path')
                # if not filemask:
                #     message.append('Invalid Source File Mask')
                if not delimiter or delimiter not in ['|', ',', '/', '#', '\t']:
                    message.append('Invalid Source File delimiter')

            elif conn_type in ['Salesforce']:
                if not query:
                    message.append('Invalid Query')
                sfquery = query.get('')
            else:
                message.append('Invalid Source Connector')

    else:
        """
            assume rec_type == 'D
        """
        if not conn_id or not conn_name or not conn_type:
            message.append('Invalid Destination Connector')
        elif conn_type == 'Salesforce':
            if not transaction_type or transaction_type not in ['insert', 'update', 'upsert']:
                message.append('Invalid Source Transaction Type')
            elif transaction_type == 'upsert' and not key_field:
                message.append('Invalid Source Key field for upsert')
        elif conn_type in ['File', 'AWS_S3']:
            if not filestartwith or not fileendwith:
                message.append('Invalid Destination File name')
            if not filepath and conn_type == 'AWS_S3':
                message.append('Invalid Destination File Path')
            if not delimiter or delimiter not in ['|', ',', '/', '#', '\t']:
                message.append('Invalid Source File delimiter')

    if not model:
        message.append('Invalid model name')

    if message:
        return [message, None]
    """
        let's generate config object
    """
    try:
        int(bulk_count)
    except Exception:
        bulk_count = settings.BULK_COUNT

    if not delimiter or delimiter not in ['|', ',']:
        delimiter = ','
    if not encoding:
        encoding = 'utf-8'
    else:
        """
            this will change when we have coded for more encoding type
        """
        encoding = 'utf-8'

    if not lineterminator:
        lineterminator = 'LF'

    from core.models.coreproxy import JobConfigProxy
    from core.models.coreproxy import ConnectorProxy
    conn_recs = ConnectorProxy.objects.filter(
        name=conn_name
    )
    if not conn_recs:
        message.append('Connector not found')
        return [message, None]
    conn_object = conn_recs[0]

    job_config = None
    """
        existing job
    """
    config_query = Q(
        Q(job_id=job_record.job.object_id) & Q(rec_type=config_type)
    )
    job_configs = JobConfigProxy.objects.filter(
        config_query
    )
    if job_configs:
        job_config = job_configs[0]

    if job_config:
        job_config.sys_update_date = timezone.now()
        job_config.user_id = user_id
        job_config.job = job_record
        job_config.rec_type = config_type
        job_config.conn_object = conn_object
        job_config.filepath = filepath
        job_config.filestartwith = filestartwith
        job_config.fileendwith = fileendwith
        job_config.filemask = filemask
        job_config.delimiter = delimiter
        job_config.encoding = encoding
        job_config.lineterminator = lineterminator
        job_config.archivepath = archivepath
        job_config.key_field = key_field
        job_config.bulk_count = bulk_count
        job_config.query = query
        job_config.transaction_type = transaction_type
        job_config.model = model

    else:
        job_config = JobConfigProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            job=job_record,
            rec_type=config_type,
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
            query=query,
            transaction_type=transaction_type,
            model=model
        )

    job_config.save()
    return [None, job_config]


def validate_model(user_id, connector, model_name):
    """
        validate model
    """
    from core.models.coreproxy import DmodelsProxy

    """
        save each model
        first we check if the object exists
    """
    dmodel = None

    recs = DmodelsProxy.objects.filter(
        conn_object_id=connector.object.object_id,
        name=model_name)
    if not recs:
        dmodel = DmodelsProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            conn_object=connector,
            name=model_name
        )
        dmodel.save()
    else:
        dmodel = recs[0]
        dmodel.sys_update_date = timezone.now()
        dmodel.user_id = user_id
        dmodel.save()

    return [None, dmodel]


def validate_map(user_id, source_config, dest_config, mapdetails):
    """
        validate mapdetails
    """
    message = []
    # job_id = config.get('job_id', None)
    if not mapdetails or len(mapdetails) < 0:
        message.append('Invalid map details')
        return [message, None]

    # first_rec = mapdetails[0]
    # source_model = cleanfield(first_rec.get('source_model', None))
    # dest_model = cleanfield(first_rec.get('dest_model', None))
    # if not source_model or not dest_model:
    #     message.append('Invalid Model in mapping')
    #     return [message, None]

    # validate_model(user_id, source_config.conn_object, source_model)
    # validate_model(user_id, dest_config.conn_object, dest_model)

    from core.models.coreproxy import DimMapTypeProxy, ModelMapProxy

    """
        remove existing records
    """
    ModelMapProxy.objects.filter(
        job_id=source_config.job.job_id
    ).delete()
    model_maprecords = []
    for idx, mapdetail in enumerate(mapdetails):
        source_model = cleanfield(mapdetail.get('source_model', None))
        source_field = cleanfield(mapdetail.get('source_field', None))
        map_type = cleanfield(mapdetail.get('map_type', ''))
        map_value = cleanfield(mapdetail.get('map_value', None))
        lookup_model = cleanfield(mapdetail.get('lookup_model', None))
        lookup_join_field = cleanfield(
            mapdetail.get('lookup_join_field', None))
        lookup_return_field = cleanfield(
            mapdetail.get('lookup_return_field', None))
        dest_model = cleanfield(mapdetail.get('dest_model', None))
        dest_field = cleanfield(mapdetail.get('dest_field', None))

        # if not source_model:
        #     message.append('Invalid Source Model at record' + str(idx))
        if not source_field:
            message.append('Invalid Source Field at record' + str(idx))

        map_type = map_type.strip()
        dim_map_type = DimMapTypeProxy.objects.get_or_none(
            map_type=map_type
        )
        if not dim_map_type:
            message.append('Invalid Map Type at record' + str(idx))

        if map_type != '' and map_type == 'constant' and not map_value:
            message.append(
                'Invalid Map Value for constant at record' + str(idx))

        if lookup_model and (not lookup_join_field or not lookup_return_field):
            message.append('Invalid Lookup details at record' + str(idx))
        if not dest_model:
            message.append('Invalid Destination Model at record' + str(idx))
        if not dest_field:
            message.append('Invalid Destination Field at record' + str(idx))

        if message:
            return [message, None]

        model_map = ModelMapProxy(
            sys_creation_date=timezone.now(),
            user_id=user_id,
            job=source_config.job,
            source_model=source_model,
            source_field=source_field,
            map_type=dim_map_type,
            map_value=map_value,
            lookup_model=lookup_model,
            lookup_join_field=lookup_join_field,
            lookup_return_field=lookup_return_field,
            dest_model=dest_model,
            dest_field=dest_field,
            errormsg=None
        )
        model_map.save()

        model_maprecords.append(model_map)

    return [None, model_maprecords]


def validate_fields(user_id, config, fields, model_rec):
    """
        validate field
    """
    message = []
    if not config:
        message.append('Configuration missing')
        return [message, None]

    if not fields:
        message.append('field details missing')
        return [message, None]

    from core.models.coreproxy import DmodelsProxy, FieldsProxy

    # model_name = cleanfield(fields[0].get('model_name', None))
    # if not model_name:
    #     message.append('field model details missing')
    #     return [message, None]

    # model_rec = DmodelsProxy.objects.get_or_none(
    #     conn_object_id=config.conn_object.object.object_id,
    #     name=model_name)
    # if not model_rec and config.conn_object.conn_name in ['Salesforce', 'Postgres']:
    #     message.append('Field Model configuration missing')
    #     return [message, None]
    # elif config.conn_object.conn_name in ['File', 'AWS_S3']:
    #     model_rec = DmodelsProxy(
    #         sys_creation_date=timezone.now(),
    #         user_id=user_id,
    #         conn_object=config.conn_object,
    #         name=model_name
    #     )
    #     model_rec.save()

    records = []

    for idx, field in enumerate(fields):
        model_name = cleanfield(field.get('model_name', None))
        field_name = cleanfield(field.get('field_name', None))
        field_type = cleanfield(field.get('field_type', 'Auto'))
        field_length = cleanfield(field.get('field_length', None))
        # field_format = cleanfield(field.get('field_format', None))
        label = cleanfield(field.get('label', None))
        primary_key = cleanfield(field.get('primary_key', None))

        if not model_name or not field_name:
            message.append('Invalid Field at record' + str(idx))

        if message:
            return [message, None]

        frecord = FieldsProxy.objects.get_or_none(
            model=model_rec,
            field_name=field_name)

        if frecord:
            frecord.sys_update_date = timezone.now()
            frecord.user_id = user_id
            frecord.field_name = field_name
            frecord.field_type = field_type
            frecord.field_length = field_length
            frecord.label = label
            frecord.primary_key = primary_key
        else:
            frecord = FieldsProxy(
                sys_creation_date=timezone.now(),
                user_id=user_id,
                model=model_rec,
                field_name=field_name,
                field_type=field_type,
                field_length=field_length,
                label=label,
                primary_key=primary_key
            )
        frecord.save()
        records.append(frecord)

    return [None, records]


@sync_to_async
def executejobbyfile(
        job_controller, filepath,
        filename, delimiter, lineterminator):
    """
        execute job
    """
    print('executing job')
    _ = job_controller.executebyfile(
        filepath, filename,
        delimiter, lineterminator
    )


async def setexecutejobbyfile(
        job_controller, filepath,
        filename, delimiter, lineterminator):
    asyncio.ensure_future(
        executejobbyfile(
            job_controller, filepath,
            filename, delimiter, lineterminator))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def runjobbyfile(request):
    """
        job run details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    response_record.status = 'ok'

    inputfile = None
    if request.FILES['document']:
        inputfile = request.FILES['document']

    if not inputfile:
        response_record.status = 'error'
        response_record.message.append('Input file is missing or corrupt')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    if inputfile.content_type not in ['application/vnd.ms-excel', 'text/plain', 'text/csv']:
        """
            not supported file type
        """
        response_record.status = 'error'
        response_record.message.append(
            'Invalid file type, only csv is supported')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    delimiter = request.POST.get('delimiter', None)
    if not delimiter or delimiter not in ['|', ',', '/', '#', '\\t']:
        response_record.status = 'error'
        response_record.message.append('Invalid delimter')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    lineterminator = request.POST.get('lineterminator', None)
    if not lineterminator or lineterminator not in ['CRLF', 'CR', 'LF']:
        response_record.status = 'error'
        response_record.message.append('Invalid line terminator')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    job_id = request.POST.get('job_id', None)
    if not job_id:
        response_record.status = 'error'
        response_record.message.append('Input Job id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    try:
        job_id = int(job_id)
    except Exception:
        response_record.status = 'error'
        response_record.message.append('Input Job id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    run_date = date(2020, 1, 1)
    from core.services.documents import DocumentsService

    document_service = DocumentsService()
    document_service.user_id = user_id
    document_service.delimiter = delimiter
    document_service.lineterminator = lineterminator
    try:
        local_file = document_service.process_document(inputfile, 'N')
        if not local_file:
            message = 'Error reading document'
            response_record.status = 'error'
            response_record.message.append(message)
            return HttpResponse(response_record.dumpoutput(),
                                content_type='application/javascript; charset=utf8')

    except Exception:
        message = 'Error reading document'
        response_record.status = 'error'
        response_record.message.append(message)
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    """
        let's get user's job details
    """
    from core.controller.jobcontroller import JobController

    job_controller = JobController(
        user_id=user_id,
        job_id=job_id,
        run_date=run_date
    )
    job_controller.schedule_id = 1
    job_controller.schedulelog_id = -1

    filename = os.path.basename(local_file)
    filepath = os.path.dirname(local_file)
    # job_controller.download_path = filepath
    # job_controller.download_file = filename
    asyncio.run(setexecutejobbyfile(
        job_controller, filepath, filename, delimiter, lineterminator))
    response_record.message.append(
        'Job run in background, Please check log for latest update')
    response_record.status = 'ok'

    # try:
    #     return_status = job_controller.executebyfile(
    #         filepath, filename,
    #         delimiter, lineterminator
    #     )
    #     if not return_status:
    #         response_record.status = 'error'
    #         response_record.message.append(message)
    #     else:
    #         response_record.status = 'ok'
    #         response_record.message.append('Error running job')

    # except SIDException as exp:
    #     message = str(exp)
    #     response_record.status = 'error'
    #     response_record.message.append(message)
    # except Exception:
    #     response_record.status = 'error'
    #     response_record.message.append('Error running job')

    response_record.setrecords(records)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@sync_to_async
def executejobbyjobrunid(user_id, job_id, jobrun_id, run_date):
    """
        execute job
    """
    response_record = ApiResponse()
    # records = {}

    from core.controller.jobcontroller import JobController
    job_controller = JobController(
        user_id=user_id
    )
    job_controller.run_date = run_date
    job_controller.rerun_flag = 'Y'
    job_controller.job_id = job_id
    try:
        job_controller.reprocess_failures(jobrun_id)
    except SIDException as exp:
        message = str(exp)
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record
    except Exception as exp:
        message = 'Error running job'
        response_record.status = 'error'
        response_record.message.append(message)
        return response_record

    return response_record


async def setexecutejobbyjobrunid(user_id, job_id, jobrun_id, run_date):
    asyncio.ensure_future(executejobbyjobrunid(
        user_id, job_id, jobrun_id, run_date))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def runjobbyjobrunid(request):
    """
        job run details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    # user_id = 'admin'
    run_date = request.GET.get('rundate', None)
    job_id = request.GET.get('job_id', None)
    jobrun_id = request.GET.get('jobrun_id', None)
    if not job_id:
        response_record.status = 'error'
        response_record.message.append('Input Job id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    if not not jobrun_id:
        response_record.status = 'error'
        response_record.message.append('Input Job run id missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    run_date = date(2020, 1, 1)
    """
        let's get user's job details
    """
    asyncio.run(setexecutejobbyjobrunid(user_id, job_id, jobrun_id, run_date))

    # response_record.setrecords(records)
    response_record.message.append(
        'Job run in background, Please check log for latest update')
    response_record.status = 'ok'
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
