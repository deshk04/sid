PROJECT_ROOT_PATH = '/sid'
# Log related settings

# logging level
LOGGING_LEVEL = 10
LOGGING_SCREEN = True
LOG_PATH = PROJECT_ROOT_PATH + '/ops/logs/apps/'
LOG_DAYS = -365

SYSTEM_USER = 'system'
SID_ADMIN = 'admin'

DJANGO_PATH = PROJECT_ROOT_PATH + '/src/django/web'

DOCUMENT_PATH = PROJECT_ROOT_PATH + '/external/documents/'
LOGFILE_PATH = DOCUMENT_PATH + 'logfiles/'
BULK_COUNT = 200

# EMail setting
SCHEDULE_EMAIL = False
JOB_EMAIL = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'sid@localhost.com'
ADMIN = [('admin', 'sid@localhost.com')]
EMAIL_SUBJECT_PREFIX = '[SID]'

EMAIL_FROM = ['noreply@localhost.com']
EMAIL_SUPPORT = ['noreply@localhost.com']

SCHEDULE_PARALLEL = False
SFOPTIMIZE = True
PARALEL_COUNT = 1
# file size in MB
SFLOOKUP_FILESIZE = 0

EXCLUDE_LOG_MODULES = ['django.db.backends.schema',
                       'django.db.backends.schema',
                       'urllib3.util.retry',
                       'django.security',
                       'salesforce',
                       'salesforce.backend',
                       'django',
                       'django.request',
                       'django.security.csrf',
                       'urllib3',
                       'salesforce.dbapi',
                       'urllib3.connection',
                       'MARKDOWN',
                       'salesforce.dbapi.driver',
                       'urllib3.contrib',
                       'salesforce.models',
                       'salesforce.auth',
                       'urllib3.response',
                       'requests',
                       'django.server',
                       'django.db.backends',
                       'django.db',
                       'urllib3.util',
                       'urllib3.poolmanager',
                       'urllib3.contrib.pyopenssl',
                       'urllib3.connectionpool',
                       'boto3',
                       'botocore',
                       's3transfer'
                       ]
