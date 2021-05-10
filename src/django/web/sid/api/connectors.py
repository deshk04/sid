import json
from datetime import datetime
from django.utils import timezone

from django.http import HttpResponse
from django.db.models import Q, F, DateField
from django.db.models import Subquery
from django.db.models.functions import Cast
from django.core.validators import validate_email

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from sid.helper.apiresponse import ApiResponse
from core.general.sidhelper import cleanfield
from core.general.sidcrypt import SIDEncryption
from core.general.exceptions import SIDException


def fetchconnectors(user_id):
    """
        connection details
    """
    from core.models.coreproxy import ConnectorProxy

    """
        fetch all connector objects
    """
    query = Q(Q(object__object_owner=user_id) & Q(
        object__object_type='Connector') & Q(
            Q(object__expiration_date__gte=datetime.today()) | Q(
                object__expiration_date__isnull=True)
    )
    )

    records = ConnectorProxy.objects.filter(
        query
    ).values('object_id', 'name', 'conn_name',
             'conn_system_type',
             'conn_name__conn_logo_path',
             'sys_creation_date', 'sys_update_date').annotate(
        id=F('object_id'),
        conn_logo=F('conn_name__conn_logo_path'),
        create_date=Cast('sys_creation_date', DateField()),
        modified_date=F('sys_update_date'),
        conn_type=F('conn_name')
    ).values(
                 'id', 'name', 'conn_type',
                 'conn_system_type', 'conn_logo',
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


def fetchsfauth(user_id):
    """
        salesforce connector details
    """
    from core.models.coreproxy import ConnectorProxy, AuthSalesforceProxy

    """
        fetch all connector objects
    """
    query = Q(Q(object__object_owner=user_id) & Q(
        object__object_type='Connector') & ~Q(name='SidLocal') & Q(
            Q(object__expiration_date__gte=datetime.today()) | Q(
                object__expiration_date__isnull=True)
    )
    )
    conn_records = ConnectorProxy.objects.filter(query)

    records = AuthSalesforceProxy.objects.filter(
        conn_object_id__in=Subquery(conn_records.values('object_id'))
    ).values('conn_object__object_id', 'conn_object__name',
             'auth_username', 'auth_password', 'security_token',
             'auth_host',
             'organisation_id').annotate(
        id=F('conn_object__object_id'),
        name=F('conn_object__name')
    ).values('id', 'name', 'auth_username', 'auth_password',
             'security_token', 'auth_host',
                 'organisation_id')

    sid_crypt = SIDEncryption()

    for record in records:
        record['auth_username'] = sid_crypt.decrypt(record['auth_username'])
        record['auth_password'] = sid_crypt.decrypt(record['auth_password'])
        record['security_token'] = sid_crypt.decrypt(record['security_token'])

    result = list(records)

    return result


def fetchs3auth(user_id):
    """
        salesforce connector details
    """
    from core.models.coreproxy import ConnectorProxy, AuthAwsS3Proxy

    """
        fetch all connector objects
    """
    query = Q(
        Q(object__object_owner=user_id) & Q(
            object__object_type='Connector') & ~Q(name='SidLocal') & Q(
                Q(object__expiration_date__gte=datetime.today()) | Q(
                    object__expiration_date__isnull=True)
        )
    )
    conn_records = ConnectorProxy.objects.filter(query)

    records = AuthAwsS3Proxy.objects.filter(
        conn_object_id__in=Subquery(conn_records.values('object_id'))
    ).values('conn_object__object_id', 'conn_object__name',
             'aws_access_key_id', 'aws_secret_access_key',
             'bucket_name', 'aws_region').annotate(
        id=F('conn_object__object_id'),
        name=F('conn_object__name')
    ).values('id', 'name', 'aws_access_key_id', 'aws_secret_access_key',
             'bucket_name', 'aws_region')

    sid_crypt = SIDEncryption()

    for record in records:
        record['aws_access_key_id'] = sid_crypt.decrypt(
            record['aws_access_key_id'])
        record['aws_secret_access_key'] = sid_crypt.decrypt(
            record['aws_secret_access_key'])

    result = list(records)

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getconnectors(request):
    """
        connection details
    """
    response_record = ApiResponse()
    records = {}
    user_id = request.user.username

    records['connectors'] = fetchconnectors(user_id)
    records['sfauth'] = fetchsfauth(user_id)
    records['s3auth'] = fetchs3auth(user_id)

    """
        let's get user's connector
    """

    response_record.setrecords(records)

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )


def updatesfconnector(body, user_id):
    """
        function is used for both update and new connector
    """
    response_record = ApiResponse()
    model_recs = None
    # response = {}
    response_record.status = 'ok'

    """
        get all field values
    """
    # conn_id = body.get('conn_id', None)
    query_type = body.get('query_type', 'new')
    name = cleanfield(body.get('name', None))
    conn_name = 'Salesforce'
    conn_system_type = cleanfield(body.get('conn_system_type', None))
    auth_username = cleanfield(body.get('auth_username', None))
    auth_password = cleanfield(body.get('auth_password', None))
    security_token = cleanfield(body.get('security_token', None))
    # organisation_id = cleanfield(body.get('organisation_id', None))
    auth_host = cleanfield(body.get('auth_host', None))
    # oauth_key = cleanfield(body.get('oauth_key', None))

    """
        check if the required fields are populated
    """
    if not name or not conn_system_type or not query_type or \
            not auth_username or not auth_password:
        """
            error
        """
        response_record.status = 'error'
        response_record.message.append('Mandatory fields missings')

    if len(name.strip()) < 2:
        response_record.status = 'error'
        response_record.message.append(
            'Connection name should me more than 1 character')
    name = name.strip().lower()

    """
        check if the username is email
    """
    try:
        validate_email(auth_username)
    except Exception:
        response_record.status = 'error'
        response_record.message.append(
            'Invalid username: should be an email address')

    if response_record.status == 'error':
        return response_record

    """
        we check the connection with salesforce
    """
    try:

        from core.connectors.salesforce.client import SalesforceClient

        sfclient = SalesforceClient()
        sfclient.authenticate(
            username=auth_username,
            password=auth_password,
            secrettoken=security_token,
            conn_system_type=conn_system_type
        )
        if not sfclient.sfconn:
            response_record.status = 'error'
            response_record.message.append(
                'Connection error with salesforce please check the credentials')
    except Exception:
        response_record.status = 'error'
        response_record.message.append(
            'Connection error with salesforce please check the credentials')

    if response_record.status == 'error':
        return response_record

    """
        if this is new connector then make sure the name does not conflict
        with other connector
    """
    if query_type == 'new':
        from core.models.coreproxy import ConnectorProxy
        query = Q(Q(object__object_owner=user_id) & Q(
            object__object_type='Connector') & Q(name=name) & Q(
                Q(object__expiration_date__gte=datetime.today()) | Q(
                    object__expiration_date__isnull=True)
        )
        )
        conn_recs = ConnectorProxy.objects.filter(query)
        if conn_recs:
            response_record.status = 'error'
            response_record.message.append(
                'Connetor name conflit with another connector')
            return response_record
    else:
        """
            make sure connector name does not conflict with another name
            from different type
        """
        pass

    """
        connector mapper
    """
    from core.mapper.connectormapper import ConnectorMapper

    try:
        """
            connector mapper does all the checks and mapping of attributes
            to model
        """
        conn_mapper = ConnectorMapper(
            user_id=user_id,
            name=name,
            conn_name=conn_name,
            conn_system_type=conn_system_type
        )

        conn_mapper.map()
        """
            store authentication details
            encrypt the data
        """
        from core.general.sidcrypt import SIDEncryption

        sid_crypt = SIDEncryption()
        auth_username = sid_crypt.encrypt(auth_username)
        auth_password = sid_crypt.encrypt(auth_password)
        security_token = sid_crypt.encrypt(security_token)

        from core.models.coreproxy import AuthSalesforceProxy

        auth_record = AuthSalesforceProxy.objects.get_or_none(
            conn_object_id=conn_mapper.connector.object_id
        )
        """
            if authenticator is not available then create a new one
        """
        if not auth_record:

            auth_record = AuthSalesforceProxy(
                sys_creation_date=timezone.now(),
                user_id=user_id,
                auth_username=auth_username,
                auth_password=auth_password,
                security_token=security_token,
                auth_host=auth_host
            )

        else:
            auth_record.sys_update_date = timezone.now()
            auth_record.user_id = user_id
            auth_record.auth_username = auth_username
            auth_record.auth_password = auth_password
            auth_record.security_token = security_token
            auth_record.auth_host = auth_host

        try:
            auth_record.conn_object_id = conn_mapper.connector.object_id
            auth_record.save()
        except Exception:
            raise SIDException('Error storing in database', 'object')

        if model_recs:
            conn_mapper.mapmodels(model_recs)

    except SIDException as sexp:
        response_record.status = 'error'
        response_record.message.append(str(sexp))
    except Exception:
        response_record.status = 'error'
        response_record.message.append('Error: storing object')

    if response_record.status != 'error':
        response_record.message.append('Record saved')

    return response_record


def updates3connector(body, user_id):
    """
        function is used for both update and new connector
    """
    response_record = ApiResponse()
    # model_recs = None
    # response = {}
    response_record.status = 'ok'

    """
        get all field values
    """
    # conn_id = body.get('conn_id', None)
    query_type = body.get('query_type', 'new')
    name = cleanfield(body.get('name', None))
    conn_name = 'AWS_S3'
    conn_system_type = cleanfield(body.get('conn_system_type', None))
    aws_access_key_id = cleanfield(body.get('aws_access_key_id', None))
    aws_secret_access_key = cleanfield(body.get('aws_secret_access_key', None))
    bucket_name = cleanfield(body.get('bucket_name', None))
    aws_region = cleanfield(body.get('aws_region', None))

    """
        check if the required fields are populated
    """
    if not name or not conn_system_type or not query_type or \
            not aws_access_key_id or not aws_secret_access_key or \
            not bucket_name:
        """
            error
        """
        response_record.status = 'error'
        response_record.message.append('Mandatory fields missings')

    if len(name.strip()) < 2:
        response_record.status = 'error'
        response_record.message.append(
            'Connection name should me more than 1 character')
    name = name.strip().lower()

    """
        we check the connection with aws s3
    """
    try:

        from core.connectors.awss3.client import AwsS3Client

        s3client = AwsS3Client()
        s3client.authenticate(
            aws_access_key_id,
            aws_secret_access_key,
            bucket_name,
            aws_region
        )
        if not s3client.s3:
            response_record.status = 'error'
            response_record.message.append(
                'Connection error with s3 please check the credentials')
    except Exception:
        response_record.status = 'error'
        response_record.message.append(
            'Connection error with s3 please check the credentials')

    if response_record.status == 'error':
        return response_record

    """
        if this is new connector then make sure the name does not conflict
        with other connector
    """
    if query_type == 'new':
        from core.models.coreproxy import ConnectorProxy
        query = Q(Q(object__object_owner=user_id) & Q(
            object__object_type='Connector') & Q(name=name) & Q(
                Q(object__expiration_date__gte=datetime.today()) | Q(
                    object__expiration_date__isnull=True)
        )
        )
        conn_recs = ConnectorProxy.objects.filter(query)
        if conn_recs:
            response_record.status = 'error'
            response_record.message.append(
                'Connetor name conflit with another connector')
            return response_record
    else:
        """
            make sure connector name does not conflict with another name
            from different type
        """
        pass

    """
        connector mapper
    """
    from core.mapper.connectormapper import ConnectorMapper

    try:
        """
            connector mapper does all the checks and mapping of attributes
            to model
        """
        conn_mapper = ConnectorMapper(
            user_id=user_id,
            name=name,
            conn_name=conn_name,
            conn_system_type=conn_system_type
        )

        conn_mapper.map()
        """
            store authentication details
        """
        from core.models.coreproxy import AuthAwsS3Proxy
        """
            encrypt the data
        """
        from core.general.sidcrypt import SIDEncryption

        sid_crypt = SIDEncryption()
        aws_access_key_id = sid_crypt.encrypt(aws_access_key_id)
        aws_secret_access_key = sid_crypt.encrypt(aws_secret_access_key)

        auth_record = AuthAwsS3Proxy.objects.get_or_none(
            conn_object_id=conn_mapper.connector.object_id
        )
        """
            if authenticator is not available then create a new one
        """
        if not auth_record:

            auth_record = AuthAwsS3Proxy(
                sys_creation_date=timezone.now(),
                user_id=user_id,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                bucket_name=bucket_name,
                aws_region=aws_region,
                write_permission=None
            )

        else:
            auth_record.sys_update_date = timezone.now()
            auth_record.user_id = user_id
            auth_record.aws_access_key_id = aws_access_key_id
            auth_record.aws_secret_access_key = aws_secret_access_key
            auth_record.bucket_name = bucket_name
            auth_record.aws_region = aws_region
            auth_record.write_permission = None

            auth_record.conn_object = conn_mapper.connector
            auth_record.save()

    except SIDException as sexp:
        response_record.status = 'error'
        response_record.message.append(str(sexp))
    except Exception:
        response_record.status = 'error'
        response_record.message.append('Error: storing object')

    if response_record.status != 'error':
        response_record.message.append('Record successful')

    return response_record


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateconnector(request):
    """
        function is used for both update and new connector
    """
    response_record = ApiResponse()

    if request.body != b'':
        body = json.loads(request.body.decode('utf-8'))
    else:
        """
            Error
        """
        response_record.status = 'error'
        response_record.message.append('No POST Data')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    """
        get all field values
    """
    conn_name = cleanfield(body.get('conn_type', None))
    user_id = request.user.username

    """
        check if the required fields are populated
    """
    errorFlag = False
    if not conn_name:
        """
            error
        """
        errorFlag = True

    from core.models.coreproxy import DimConnectorProxy

    record = DimConnectorProxy.objects.get_or_none(
        conn_name=conn_name
    )
    if not record:
        errorFlag = True

    if errorFlag:
        response_record.status = 'error'
        response_record.message.append(
            'Mandatory fields missings: Connector Type')

        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )
    """
        we can call the appr connector function
    """
    if conn_name == 'Salesforce':
        response_record = updatesfconnector(body, user_id)
    elif conn_name == 'AWS_S3':
        response_record = updates3connector(body, user_id)
    else:
        response_record.status = 'error'
        response_record.message.append(
            'Connector not supported')

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
