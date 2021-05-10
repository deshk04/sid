import os
from datetime import datetime

from django.http import HttpResponse
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from sid.helper.apiresponse import ApiResponse


def fetchs3details(conn_id, user_id):
    """
        s3 details
    """
    from core.models.coreproxy import ConnectorProxy

    result = []
    """
        fetch all connector objects
    """
    query = Q(Q(object__object_owner=user_id) & Q(
        object__object_type='Connector') & Q(
            object_id=conn_id) & Q(
                Q(object__expiration_date__gte=datetime.today()) | Q(
                    object__expiration_date__isnull=True)
    )
    )
    conn_records = ConnectorProxy.objects.filter(query)
    if not conn_records:
        return result

    try:
        from core.connectors.awss3.client import AwsS3Client

        s3client = AwsS3Client()
        s3client.getclient(conn_records[0])

        from core.services.awss3 import AwsS3Service
        s3_service = AwsS3Service()
        s3_service.s3client = s3client
        s3_service.bucket_name = s3client.bucket_name
        s3_service.setup()
        output = s3_service.getTreeView()
        result.append(output)
        # print(json.dumps(output, indent=2))
    except Exception:
        return result

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gets3tree(request):
    """
        connection details
    """
    response_record = ApiResponse()
    records = {}
    response_record.status = 'ok'

    user_id = request.user.username
    # user_id = 'admin'
    conn_id = request.GET.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Input connector missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    records['tree'] = fetchs3details(conn_id, user_id)

    """
        let's get user's connector
    """
    response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def fetchs3file(conn_id, filename, user_id):
    """
        s3 details
    """
    from core.models.coreproxy import ConnectorProxy

    result = None
    """
        fetch all connector objects
    """
    query = Q((Q(object__object_owner=user_id) | Q(
        object__object_owner='admin')) & Q(
            object__object_type='Connector') & Q(
                object_id=conn_id) & Q(
                    Q(object__expiration_date__gte=datetime.today()) | Q(
                        object__expiration_date__isnull=True)
    )
    )
    conn_records = ConnectorProxy.objects.filter(query)
    if not conn_records:
        return result

    try:

        from core.connectors.awss3.client import AwsS3Client
        s3client = AwsS3Client()
        s3client.getclient(conn_records[0])

        from core.services.awss3 import AwsS3Service
        s3_service = AwsS3Service()
        s3_service.s3client = s3client
        s3_service.s3_bucket = s3client.s3_bucket
        s3_service.bucket_name = s3client.bucket_name
        s3_service.user_id = user_id
        s3_service.setup()
        file_path = os.path.dirname(filename)
        filestartname = os.path.basename(filename)
        return_file = s3_service.fetchfilefrompath(file_path, filestartname)
        if return_file:
            """
                send the downloaded filename
            """
            # return_file = os.path.basename(return_file)
            result = return_file
    except Exception:
        return result

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gets3file(request):
    """
        s3 file details
    """
    response_record = ApiResponse()
    response_record.status = 'ok'

    user_id = request.user.username
    # user_id = 'admin'
    conn_id = request.GET.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Input connector missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    filename = request.GET.get('filename', None)
    if not filename:
        response_record.status = 'error'
        response_record.message.append('Input filename missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    return_file = fetchs3file(conn_id, filename, user_id)
    if not return_file:
        response_record.status = 'error'
        response_record.message.append('file not found')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    """
        download the file for user
    """
    with open(return_file, 'rb') as handle:
        response = HttpResponse(handle.read(),
                                content_type='text/csv')
        content_text = 'attachment; filename=' + os.path.basename(return_file)
        response['Content-Disposition'] = content_text
        return response
