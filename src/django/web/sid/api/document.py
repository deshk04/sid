from datetime import datetime

from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.general.exceptions import SIDException
from sid.helper.apiresponse import ApiResponse
from core.general import settings


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def localdocument(request):
    """
        process local file
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
        response_record.message.append('Invalid file type, only csv is supported')
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

    from core.services.documents import DocumentsService

    document_service = DocumentsService()
    document_service.user_id = user_id
    document_service.delimiter = delimiter
    document_service.lineterminator = lineterminator
    try:
        fields = document_service.process_document(inputfile)
        if not fields:
            response_record.status = 'error'
            response_record.message.append('Error parsing header in the document')
            return HttpResponse(response_record.dumpoutput(),
                                content_type='application/javascript; charset=utf8')

        records['document'] = fields
        records['config'] = document_service.get_docodetails()
    except Exception:
        pass

    response_record.records = records

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def s3document(request):
    """
        process local file
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username
    response_record.status = 'ok'

    conn_id = request.POST.get('conn_id', None)
    if not conn_id:
        response_record.status = 'error'
        response_record.message.append('Input connector missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    inputfile = request.POST.get('document', None)
    if not inputfile:
        response_record.status = 'error'
        response_record.message.append('Input file is missing or corrupt')
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

    from sid.api.awss3 import fetchs3file
    return_file = fetchs3file(conn_id, inputfile, user_id)
    if not return_file:
        response_record.status = 'error'
        response_record.message.append('File not found')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    """
        get s3 connector object
    """

    from core.services.documents import DocumentsService

    document_service = DocumentsService()
    document_service.user_id = user_id
    document_service.delimiter = delimiter
    document_service.lineterminator = lineterminator
    try:
        fields = document_service.process_s3document(return_file)
        if not fields:
            response_record.status = 'error'
            response_record.message.append('Error parsing header in the document')
            return HttpResponse(response_record.dumpoutput(),
                                content_type='application/javascript; charset=utf8')

        records['document'] = fields
        document_service.set_filename(inputfile)
        records['config'] = document_service.get_docodetails()
    except Exception:
        pass

    response_record.records = records

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
