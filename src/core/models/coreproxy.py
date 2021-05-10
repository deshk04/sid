"""
  Description:    Proxy modules for django orm
"""

from django.db import models

from sid.models import AuthSalesforce, Connector, Dmodels
from sid.models import Fields, Jobs, ModelMap, Object
from sid.models import DimConnector, DimSystemType, DimMapType, DimFileMask
from sid.models import AuthAwsS3, JobrunDetails, JobrunLog
from sid.models import JobConfig, JobDistribution
from sid.models import Schedule, ScheduleConfig, ScheduleLog
from sid.models import ScheduleDistribution, SidSettings


from core.models.sidmodelmanager import SIDModelManager


class AuthSalesforceProxy(AuthSalesforce):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(AuthSalesforce, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ConnectorProxy(Connector):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Connector, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class DmodelsProxy(Dmodels):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Dmodels, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class FieldsProxy(Fields):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Fields, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class JobsProxy(Jobs):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Jobs, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ModelMapProxy(ModelMap):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(ModelMap, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ObjectProxy(Object):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Object, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class DimConnectorProxy(DimConnector):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(DimConnector, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class DimFileMaskProxy(DimFileMask):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(DimFileMask, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class DimSystemTypeProxy(DimSystemType):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(DimSystemType, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class DimMapTypeProxy(DimMapType):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(DimMapType, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class AuthAwsS3Proxy(AuthAwsS3):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(AuthAwsS3, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class JobrunDetailsProxy(JobrunDetails):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(JobrunDetails, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class JobrunLogProxy(JobrunLog):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(JobrunLog, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class JobConfigProxy(JobConfig):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(JobConfig, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class JobDistributionProxy(JobDistribution):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(JobDistribution, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ScheduleProxy(Schedule):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(Schedule, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ScheduleConfigProxy(ScheduleConfig):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(ScheduleConfig, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ScheduleLogProxy(ScheduleLog):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(ScheduleLog, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class ScheduleDistributionProxy(ScheduleDistribution):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(ScheduleDistribution, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'


class SidSettingsProxy(SidSettings):
    objects = SIDModelManager()

    def __init__(self, *args, **kwargs):
        super(SidSettings, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'sid'
