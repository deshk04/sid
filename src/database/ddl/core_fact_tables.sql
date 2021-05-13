----=============================================
---- Description:  Main sid database
----=============================================


----=============================================
--  Create statements for FACT tables
----=============================================

----=============================================
--   Drop statements
----=============================================

DROP TABLE auth_database CASCADE;
DROP TABLE auth_aws_s3 CASCADE;
DROP TABLE auth_salesforce CASCADE;
DROP TABLE model_map CASCADE;
DROP TABLE jobrun_details CASCADE;
DROP TABLE jobrun_log CASCADE;
DROP TABLE jobs CASCADE;
DROP TABLE fields CASCADE;
DROP TABLE dmodels CASCADE;
DROP TABLE connector CASCADE;
DROP TABLE object CASCADE;
DROP TABLE lookup_map_details CASCADE;
DROP TABLE sid_settings;

----=============================================
--  Fact tables
----=============================================

CREATE TABLE object
(
    object_id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	object_type text,
	object_key text,
    object_owner text,
    effective_date date,
    expiration_date date

)
WITH (
    OIDS = FALSE
);


CREATE TABLE connector
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	object_id bigint REFERENCES object(object_id),
    name text,
	conn_name text REFERENCES dim_connector(conn_name),
    conn_usage text,
    conn_system_type text REFERENCES dim_system_type(system_type),
    UNIQUE(object_id)
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE auth_database
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	conn_object_id bigint REFERENCES connector(object_id),
	auth_username text,
    auth_password text,
    auth_database text,
    auth_host text,
    UNIQUE(conn_object_id)
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE auth_aws_s3
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	conn_object_id bigint REFERENCES connector(object_id),

    aws_access_key_id text,
    aws_secret_access_key text,
	bucket_name text,
    aws_region text,
    write_permission character(1),
    UNIQUE(conn_object_id)
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE auth_salesforce
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	conn_object_id bigint REFERENCES connector(object_id),

	auth_username text,
    auth_password text,
    auth_host text,
    security_token text,
    organisation_id text,
    consumer_key text,
    oauth_object_id text,

    UNIQUE(conn_object_id)
 )
WITH (
    OIDS = FALSE
);


CREATE TABLE dmodels
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	conn_object_id bigint REFERENCES connector(object_id),
    name text,
    label text,
    readable text,
    writeable text,
    UNIQUE(conn_object_id,name)
 )
WITH (
    OIDS = FALSE
);



CREATE TABLE fields
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    model_id bigint REFERENCES dmodels(id),
    field_name text,
    field_type text,
    field_length text,
    field_format text,
    label text,
    primary_key CHARACTER(1),
    choices text,
    nullable CHARACTER(1),
    UNIQUE(model_id,field_name)
 )
WITH (
    OIDS = FALSE
);


CREATE TABLE jobs
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    job_id bigint REFERENCES object(object_id),
	job_name text,
    run_type character(1), -- A: Adhoc, R: Regular
    parallel_count INTEGER,
    UNIQUE(job_id)

 )
WITH (
    OIDS = FALSE
);


CREATE TABLE job_config
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    job_id bigint REFERENCES jobs(job_id),
    rec_type CHARACTER(1) NOT NULL, -- S: Source, D: Destination
    conn_object_id bigint REFERENCES connector(object_id),
    filepath text,
    filestartwith text,
    fileendwith text,
    filemask text,
    delimiter character(1),
    encoding text,
    lineterminator text,
    archivepath text,
    key_field text,
    bulk_count integer DEFAULT 100 NOT NULL,
    query text,
    transaction_type text,
    model text,
    UNIQUE(job_id, rec_type)

 )
WITH (
    OIDS = FALSE
);

CREATE TABLE job_distribution
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    job_id bigint REFERENCES jobs(job_id),
    file_type text,
    email_flag CHARACTER DEFAULT 'N',
	tolist text,
    cclist text,
    bcclist text,
    UNIQUE(job_id)

 )
WITH (
    OIDS = FALSE
);

CREATE TABLE jobrun_log
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    job_id bigint REFERENCES jobs(job_id),
    filename text,
    file_date text,
    run_date date,
    message text,
    status text,
    total_count integer,
    success_count integer,
    failure_count integer,
    warning_count integer,
    schedule_id integer,
    schedulelog_id integer
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE jobrun_details
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    jobrun_id bigint REFERENCES jobrun_log(id),
    record_number integer,
    record_key text,
    record_value text,
    status_code text,
    status_message text,
    orig_record text,
    processed_record text
 )
WITH (
    OIDS = FALSE
);


CREATE TABLE model_map
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    job_id bigint REFERENCES jobs(job_id) NOT NULL,
    source_model text,
    source_field text NOT NULL,
    map_type text REFERENCES dim_map_type(map_type),
    map_value text,
    lookup_model text,
    lookup_join_field text,
    lookup_return_field text,
    dest_model text NOT NULL,
    dest_field text,
    errormsg text, -- incase the field is removed from model
    UNIQUE(job_id, source_field, map_type, dest_field)
 )
WITH (
    OIDS = FALSE
);


CREATE TABLE schedule
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    schedule_id bigint REFERENCES object(object_id),
    schedule_type TEXT,
    schedule_name TEXT NOT NULL,
    schedule_owner text not null,
    rerun_flag CHARACTER(1),
    frequency text not NULL,
    day_of_week text,
    month text,
    day_of_month text,
    hours text,
    minutes text,
    comment text,
    UNIQUE(schedule_id)
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE schedule_config
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    schedule_id bigint REFERENCES schedule(schedule_id),
    job_sequence integer,
    job_id BIGINT REFERENCES jobs(job_id),
    -- dependent_job_id bigint REFERENCES jobs(job_id),
    active_flag CHARACTER(1)
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE schedule_log
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    schedule_id bigint REFERENCES schedule(schedule_id),
    run_date date,
    message text,
    status text
 )
WITH (
    OIDS = FALSE
);

CREATE TABLE schedule_distribution
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    schedule_id bigint REFERENCES schedule(schedule_id),
    email_flag CHARACTER DEFAULT 'N',
	tolist text,
    cclist text,
    bcclist text,
    UNIQUE(schedule_id)

 )
WITH (
    OIDS = FALSE
);

CREATE TABLE sid_settings
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

    object_owner text,
    key text,
    value text
)
WITH (
    OIDS = FALSE
);
