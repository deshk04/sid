from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse

# from rest_framework import serializers
# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response


def index(request):
    """
        Main page
    """
    response = TemplateResponse(request,
                                'index.html', {})

    return response
