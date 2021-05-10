""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""

from django.conf.urls import url
from django.contrib import admin
# from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from sid.sidtoken import MyTokenObtainPairView

from sid.api.connectors import getconnectors
from sid.api.connectors import updateconnector
from sid.api.joblogs import getjoblogs, downloadlog, getjoblogbyid
from sid.api.schedule import getschedules, runschedule
from sid.api.schedule import getschedulelogs, getschedulebyid, updateschedule
from sid.api.dimensions import getdimensions
from sid.api.jobs import getjobs, getjobbyid, runjobbyid, runjobbyjobrunid
from sid.api.awss3 import gets3tree, gets3file
from sid.api.salesforce import getconnmodels, fetchconnmodels, validatesfquery
from sid.api.document import localdocument, s3document
from sid.api.jobs import updatejob, runjobbyfile
from sid.api.password import updatepassword

urlpatterns = [
    # url(r'^index/', index, name="index"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('sid-token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url('getconnectors/', getconnectors, name="getconnectors"),
    url('getdimensions/', getdimensions, name="getdimensions"),
    url('updateconnector/', updateconnector, name="updateconnector"),
    url('getjoblogs/', getjoblogs, name="getjoblogs"),
    url('downloadlog/', downloadlog, name="downloadlog"),
    url('getschedules/', getschedules, name="getschedules"),
    url('getjobs/', getjobs, name="getjobs"),
    url('getjobbyid/', getjobbyid, name="getjobbyid"),
    url('gets3tree/', gets3tree, name="gets3tree"),
    url('gets3file/', gets3file, name="gets3file"),
    url('runschedule/', runschedule, name="runschedule"),
    url('getschedulelogs/', getschedulelogs, name="getschedulelogs"),
    url('runjobbyid/', runjobbyid, name="runjobbyid"),
    url('getconnmodels/', getconnmodels, name="getconnmodels"),
    url('localdocument/', localdocument, name="localdocument"),
    url('fetchconnmodels/', fetchconnmodels, name="fetchconnmodels"),
    url('s3document/', s3document, name="s3document"),
    url('updatejob/', updatejob, name="updatejob"),
    url('runjobbyfile/', runjobbyfile, name="runjobbyfile"),
    url('updatepassword/', updatepassword, name="updatepassword"),
    url('runjobbyjobrunid/', runjobbyjobrunid, name="runjobbyjobrunid"),
    url('getjoblogbyid/', getjoblogbyid, name="getjoblogbyid"),
    url('getschedulebyid/', getschedulebyid, name="getschedulebyid"),
    url('validatesfquery/', validatesfquery, name="validatesfquery"),
    url('updateschedule/', updateschedule, name="updateschedules"),

]

urlpatterns += staticfiles_urlpatterns()
