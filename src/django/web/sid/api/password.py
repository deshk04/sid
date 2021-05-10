from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from sid.helper.apiresponse import ApiResponse
import json
import re


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatepassword(request):
    """
        change password
    """
    response_record = ApiResponse()
    user_id = request.user.username
    response_record.status = 'ok'

    if request.body != b'':
        body = json.loads(request.body.decode('utf-8'))
    else:
        """
            Error
        """
        response_record.status = 'error'
        response_record.message.append('Input Data is missing')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8')

    curr_passwd = body.get('curr_passwd', None)
    new_passwd1 = body.get('new_passwd1', None)
    new_passwd2 = body.get('new_passwd2', None)

    user_rec = User.objects.get(username=user_id)

    if not user_rec:
        response_record.message.append('Invalid user')

    if not user_rec.check_password(curr_passwd):
        response_record.message.append('Current Password is invalid')

    if not new_passwd1 or len(new_passwd1) < 8:
        response_record.message.append('Password must be at least 8 characters')

    if not new_passwd2 or new_passwd1 != new_passwd2:
        response_record.message.append('Password must match')

    if not bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9]).+$', new_passwd1)):
        response_record.message.append('Password must contain at least 1 letter and 1 number')

    if response_record.message:
        response_record.status = 'error'
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    try:
        user_rec.set_password(new_passwd1)
        user_rec.save()
        response_record.message.append('Password changed')
    except Exception as exp:
        response_record.status = 'error'
        response_record.message.append('Error changing password')
        return HttpResponse(response_record.dumpoutput(),
                            content_type='application/javascript; charset=utf8'
                            )

    return HttpResponse(response_record.dumpoutput(),
                        content_type='application/javascript; charset=utf8'
                        )
