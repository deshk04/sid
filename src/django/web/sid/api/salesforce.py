import os
import base64
import asyncio
from asgiref.sync import sync_to_async

from datetime import datetime, date
import json
from django.http import HttpResponse
from django.db.models import Q, F
from django.utils import timezone
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.general.exceptions import SIDException
from core.general.sidhelper import cleanfield, get_downloadpath
from sid.helper.apiresponse import ApiResponse
from core.general import settings


def getsfobjects(user_id, conn_id, model_name):
    """
        refresh sf objects
    """
    response_record = ApiResponse()
    records = {}
    response_record.status = 'ok'

    from core.services.salesforce import SalesforceService
    from sid.api.jobs import fetchjobfields

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
    query = Q(
        Q(object__object_owner=user_id) & Q(
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

    from sid.api.jobs import fetchconnectormodels, fetchjobfields
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


def fetchsfqueryresult(user_id, filter_flag, jobconfig):
    """
        fetch data from sf query
    """
    message = []
    sfrecords = []
    response = {}

    try:
        from core.connectors.salesforce.reader import Reader
        reader = Reader(
            user_id=user_id,
            run_date=None,
            config=jobconfig
        )
        reader.connect()
        reader.normalize = True
        records = reader.set_reader()
        if records:
            for record in reader.read():
                # sfrec = {
                #     'fields': reader.header,
                #     'records': record
                # }
                sfrecords.append(record)
                if filter_flag:
                    break
            response['fields'] = reader.header
            response['records'] = sfrecords
            reader.down()
        else:
            message.append('no records found')

    except SIDException as exp:
        message.append(str(exp))
    except Exception as exp:
        message.append(str(exp))

    return [message, response]


def downloadqueryresult(user_id, source_config):
    """
        fetch data from sf query
    """
    message = []
    """
        set destination connector as SidLocal
        and run the job to produce the file
    """
    fpath = get_downloadpath(user_id)
    if not os.path.isdir(fpath):
        os.mkdir(fpath)

    filename = 'sfquery' + '_' + date.today().strftime('%Y%m%d')
    fullfilename = fpath + filename + '.csv'
    """
        if file exists remove it
    """
    if os.path.isfile(filename):
        os.remove(filename)

    from core.models.coreproxy import ConnectorProxy, JobConfigProxy
    sidconnector = ConnectorProxy.objects.get_or_none(
        name='SidLocal',
        conn_name='File'
    )
    destconfig = JobConfigProxy(
        conn_object=sidconnector,
        rec_type='D',
        filepath=fpath,
        filestartwith=filename,
        fileendwith='.csv',
        delimiter=','
    )

    try:
        from core.connectors.salesforce.reader import Reader
        from core.connectors.file.writer import Writer

        reader = Reader(
            user_id=user_id,
            run_date=None,
            config=source_config
        )
        reader.connect()
        reader.normalize = True
        records = reader.set_reader()
        if records:
            writer = Writer(
                user_id=user_id,
                run_date=None,
                config=destconfig
            )
            writer.setup(reader.header)
            for record in reader.read():
                writer.write(record)

        else:
            message.append('no records found')

    except SIDException as exp:
        message.append(str(exp))
    except Exception as exp:
        message.append(str(exp))
    if reader:
        reader.down()
    if writer:
        writer.down()
    if len(message) > 0:
        return [message, None]

    record = {}
    with open(fullfilename, 'r') as handle:
        record['filedata'] = handle.read()
        record['filename'] = os.path.basename(fullfilename)

    # response = FileResponse(fpath, os.path.basename(fullfilename))
    # response['Content-Type'] = 'application/xlsx'
    # response['Content-Disposition'] = 'attachment; filename=' + self.report_filename
    # return response

    return [message, record]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validatesfquery(request):
    """
        validate SF query
    """
    response_record = ApiResponse()
    user_id = request.user.username

    # if request.body != b'':
    #     body = json.loads(request.body.decode('utf-8'))

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

    connector = body.get('connector', None)
    querydetails = body.get('query', None)
    filter_flag = body.get('filter', 'y')
    if filter_flag.lower() == 'n':
        filter_flag = False
    else:
        filter_flag = True

    download_flag = body.get('download', 'n')
    if download_flag.lower() == 'y':
        download_flag = True
    else:
        download_flag = False

    if not connector:
        response_record.status = 'error'
        response_record.message.append('Invalid connector')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')
    if not querydetails:
        response_record.status = 'error'
        response_record.message.append('Invalid Query')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    conn_id = connector.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Invalid connector')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    sfquery = querydetails.get('query', None)
    metadata = querydetails.get('metadata', None)
    if not sfquery or not metadata:
        response_record.status = 'error'
        response_record.message.append('Invalid query')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    from core.models.coreproxy import ConnectorProxy

    """
        fetch connector object
    """
    query = Q(
        Q(object__object_owner=user_id) & Q(
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

    from core.models.coreproxy import JobConfigProxy

    jobconfig = JobConfigProxy(
        user_id=user_id,
        rec_type='S',
        conn_object=conn_records[0],
        query=querydetails
    )
    errors = None
    if download_flag:
        errors, sfrecords = downloadqueryresult(user_id, jobconfig)
        response_record.records = sfrecords
    else:
        errors, sfrecords = fetchsfqueryresult(user_id, filter_flag, jobconfig)
        response_record.records = sfrecords

    if errors:
        response_record.status = 'error'
        response_record.message = errors
    else:
        response_record.status = 'ok'
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
