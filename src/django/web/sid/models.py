from django.db import models


class AuthAwsS3(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    conn_object = models.ForeignKey(
        'Connector', models.DO_NOTHING, unique=True, blank=True, null=True, to_field='object_id')
    aws_access_key_id = models.TextField(blank=True, null=True)
    aws_secret_access_key = models.TextField(blank=True, null=True)
    bucket_name = models.TextField(blank=True, null=True)
    aws_region = models.TextField(blank=True, null=True)
    write_permission = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'auth_aws_s3'


class AuthDatabase(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    conn_object = models.ForeignKey(
        'Connector', models.DO_NOTHING, unique=True, blank=True, null=True, to_field='object_id')
    auth_username = models.TextField(blank=True, null=True)
    auth_password = models.TextField(blank=True, null=True)
    auth_database = models.TextField(blank=True, null=True)
    auth_host = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'auth_database'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthSalesforce(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    conn_object = models.ForeignKey(
        'Connector', models.DO_NOTHING, unique=True, blank=True, null=True, to_field='object_id')
    auth_username = models.TextField(blank=True, null=True)
    auth_password = models.TextField(blank=True, null=True)
    auth_host = models.TextField(blank=True, null=True)
    security_token = models.TextField(blank=True, null=True)
    organisation_id = models.TextField(blank=True, null=True)
    consumer_key = models.TextField(blank=True, null=True)
    oauth_object_id = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'auth_salesforce'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Connector(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    object = models.ForeignKey('Object', models.DO_NOTHING,
                               unique=True, blank=True, null=True, to_field='object_id')
    name = models.TextField(blank=True, null=True)
    conn_name = models.ForeignKey('DimConnector', models.DO_NOTHING,
                                  db_column='conn_name', blank=True, null=True, to_field='conn_name')
    conn_usage = models.TextField(blank=True, null=True)
    conn_system_type = models.ForeignKey(
        'DimSystemType', models.DO_NOTHING, db_column='conn_system_type', blank=True, null=True, to_field='system_type')

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'connector'


class DimConnector(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    conn_name = models.TextField(unique=True, blank=True, null=True)
    conn_usage = models.TextField(blank=True, null=True)
    conn_logo_path = models.TextField(blank=True, null=True)
    conn_status = models.TextField(blank=True, null=True)
    conn_type = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_connector'


class DimFileMask(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    filemask = models.TextField(unique=True, blank=True, null=True)
    conversion = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_file_mask'


class DimMapType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    map_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_map_type'


class DimObjectType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    object_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_object_type'


class DimSystemType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    system_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_system_type'


class DimDelimiterType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    delimiter_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_delimiter_type'


class DimFieldType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    field_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_field_type'


class DimLineType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    line_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_line_type'


class DimTransactionType(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    transaction_type = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dim_transaction_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dmodels(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    conn_object = models.ForeignKey(
        Connector, models.DO_NOTHING, blank=True, null=True, related_name='+', to_field='object_id')
    name = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    readable = models.TextField(blank=True, null=True)
    writeable = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'dmodels'


class Fields(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    model = models.ForeignKey(
        Dmodels, models.DO_NOTHING, blank=True, null=True)
    field_name = models.TextField(blank=True, null=True)
    field_type = models.TextField(blank=True, null=True)
    field_length = models.TextField(blank=True, null=True)
    field_format = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    primary_key = models.CharField(max_length=1, blank=True, null=True)
    choices = models.TextField(blank=True, null=True)
    nullable = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'fields'
        unique_together = (('model', 'field_name'),)


class JobrunDetails(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    jobrun = models.ForeignKey(
        'JobrunLog', models.DO_NOTHING, blank=True, null=True)
    record_number = models.IntegerField(blank=True, null=True)
    record_key = models.TextField(blank=True, null=True)
    record_value = models.TextField(blank=True, null=True)
    status_code = models.TextField(blank=True, null=True)
    status_message = models.TextField(blank=True, null=True)
    orig_record = models.TextField(blank=True, null=True)
    processed_record = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'jobrun_details'


class JobrunLog(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING,
                            blank=True, null=True, to_field='job_id')
    filename = models.TextField(blank=True, null=True)
    file_date = models.TextField(blank=True, null=True)
    run_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    total_count = models.IntegerField()
    success_count = models.IntegerField()
    failure_count = models.IntegerField()
    warning_count = models.IntegerField()
    schedule_id = models.IntegerField()
    schedulelog_id = models.IntegerField()

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'jobrun_log'


class Jobs(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    job = models.ForeignKey('Object', models.DO_NOTHING,
                            unique=True, blank=True, null=True, to_field='object_id')
    job_name = models.TextField(blank=True, null=True)
    run_type = models.CharField(max_length=1, blank=True, null=True)
    parallel_count = models.IntegerField()

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'jobs'


class JobConfig(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING,
                            blank=True, null=True, to_field='job_id')
    rec_type = models.CharField(max_length=1)
    conn_object = models.ForeignKey(
        Connector, models.DO_NOTHING, blank=True, null=True, to_field='object_id')
    filepath = models.TextField(blank=True, null=True)
    filestartwith = models.TextField(blank=True, null=True)
    fileendwith = models.TextField(blank=True, null=True)
    filemask = models.TextField(blank=True, null=True)
    delimiter = models.CharField(max_length=1, blank=True, null=True)
    encoding = models.TextField(blank=True, null=True)
    lineterminator = models.TextField(blank=True, null=True)
    archivepath = models.TextField(blank=True, null=True)
    key_field = models.TextField(blank=True, null=True)
    bulk_count = models.IntegerField()
    query = models.TextField(blank=True, null=True)
    transaction_type = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'job_config'
        unique_together = (('job', 'rec_type'),)


class JobDistribution(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING,
                            unique=True, blank=True, null=True, to_field='job_id')
    file_type = models.TextField(blank=True, null=True)
    email_flag = models.CharField(max_length=1, blank=True, null=True)
    tolist = models.TextField(blank=True, null=True)
    cclist = models.TextField(blank=True, null=True)
    bcclist = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'job_distribution'


class ModelMap(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    job = models.ForeignKey(Jobs, models.DO_NOTHING, to_field='job_id')
    source_model = models.TextField(blank=True, null=True)
    source_field = models.TextField()
    map_type = models.ForeignKey(DimMapType, models.DO_NOTHING,
                                 db_column='map_type', blank=True, null=True, to_field='map_type')
    map_value = models.TextField(blank=True, null=True)
    lookup_model = models.TextField(blank=True, null=True)
    lookup_join_field = models.TextField(blank=True, null=True)
    lookup_return_field = models.TextField(blank=True, null=True)
    dest_model = models.TextField()
    dest_field = models.TextField(blank=True, null=True)
    errormsg = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'model_map'
        unique_together = (('job', 'source_field', 'map_type', 'dest_field'),)


class Object(models.Model):
    object_id = models.BigAutoField(primary_key=True)
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    object_type = models.TextField(blank=True, null=True)
    object_key = models.TextField(blank=True, null=True)
    object_owner = models.TextField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'object'


class Schedule(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    schedule = models.ForeignKey(
        Object, models.DO_NOTHING, unique=True, blank=True, null=True, to_field='object_id')
    schedule_type = models.TextField(blank=True, null=True)
    schedule_name = models.TextField()
    schedule_owner = models.TextField()
    rerun_flag = models.CharField(max_length=1, blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    day_of_week = models.TextField(blank=True, null=True)
    month = models.TextField(blank=True, null=True)
    day_of_month = models.TextField(blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    minutes = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'schedule'


class ScheduleConfig(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    schedule = models.ForeignKey(
        Schedule, models.DO_NOTHING, blank=True, null=True, to_field='schedule_id')
    job_sequence = models.IntegerField(blank=True, null=True)
    job = models.ForeignKey(Jobs, models.DO_NOTHING,
                            blank=True, null=True, to_field='job_id')
    active_flag = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'schedule_config'


class ScheduleLog(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    schedule = models.ForeignKey(
        Schedule, models.DO_NOTHING, blank=True, null=True, to_field='schedule_id')
    run_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'schedule_log'


class ScheduleDistribution(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    schedule = models.ForeignKey(
        Schedule, models.DO_NOTHING, unique=True, blank=True, null=True, to_field='schedule_id')
    email_flag = models.CharField(max_length=1, blank=True, null=True)
    tolist = models.TextField(blank=True, null=True)
    cclist = models.TextField(blank=True, null=True)
    bcclist = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'schedule_distribution'


class SidSettings(models.Model):
    sys_creation_date = models.DateTimeField(blank=True, null=True)
    sys_update_date = models.DateTimeField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    object_owner = models.TextField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    class Meta:
        managed = False
        db_table = 'sid_settings'
