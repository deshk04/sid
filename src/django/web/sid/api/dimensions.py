
from django.http import HttpResponse
from sid.helper.apiresponse import ApiResponse


def dimconnectors():
    """
        connector dimension tables
    """
    from sid.models import DimConnector

    records = list(DimConnector.objects.filter(
        conn_status='Active'
    ).values('conn_name', 'conn_type', 'conn_usage',
             'conn_logo_path', 'conn_status', 'description'))

    return records


def dimfilemask():
    """
        connector dimension tables
    """
    from sid.models import DimFileMask

    records = list(DimFileMask.objects.all(
    ).values('filemask', 'conversion'))

    return records


def dimmaptype():
    """
     dimension tables
    """
    from sid.models import DimMapType

    records = list(DimMapType.objects.all(
    ).values('map_type', 'description'))

    return records


def dimsystemtypes():
    """
        system type dimension tables
    """
    from sid.models import DimSystemType

    records = list(DimSystemType.objects.all(
    ).values('system_type', 'description'))

    return records


def dimdelimitertypes():
    """
        system type dimension tables
    """
    from sid.models import DimDelimiterType

    records = list(DimDelimiterType.objects.all(
    ).values('delimiter_type', 'description'))

    return records


def dimfieldtypes():
    """
        system type dimension tables
    """
    from sid.models import DimFieldType

    records = list(DimFieldType.objects.all(
    ).values('field_type', 'description'))

    return records


def dimnewlinetypes():
    """
        system type dimension tables
    """
    from sid.models import DimLineType

    records = list(DimLineType.objects.all(
    ).values('line_type', 'description'))

    return records


def dimtransactiontypes():
    """
        system type dimension tables
    """
    from sid.models import DimTransactionType

    records = list(DimTransactionType.objects.all(
    ).values('transaction_type', 'description'))

    return records


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getdimensions(request):
    """
        connection details
    """
    response_record = ApiResponse()
    dimensions = {}

    dimensions['dimconnectors'] = dimconnectors()
    dimensions['dimsystemtypes'] = dimsystemtypes()
    dimensions['dimfilemask'] = dimfilemask()
    dimensions['dimmaptype'] = dimmaptype()
    dimensions['dimfieldtype'] = dimfieldtypes()
    dimensions['dimnewlinetype'] = dimnewlinetypes()
    dimensions['dimdelimitertype'] = dimdelimitertypes()
    dimensions['dimtransactiontype'] = dimtransactiontypes()

    response_record.setrecords(dimensions)
    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
