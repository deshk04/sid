----=============================================
---- Description:  dim tables
----=============================================


----=============================================
--  Create statements for DIM tables
----=============================================


----=============================================
--   Drop statements
----=============================================

DROP TABLE dim_object_type;
DROP TABLE dim_connector_type;
DROP TABLE dim_connector_system_type;
DROP TABLE dim_map_type;
DROP TABLE dim_job_type;

DROP TABLE dim_transaction_type;
DROP TABLE dim_delimiter_type;
DROP TABLE dim_line_type;
DROP TABLE dim_field_type;

----=============================================
--   Dim tables
----=============================================

CREATE TABLE dim_object_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	object_type text,
	description text,

    UNIQUE (object_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_connector
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	conn_name text, -- Salesforce , postgres...
    conn_usage text, -- can used for source , dest or both
    conn_logo_path text, -- logo path
    conn_status text, -- Active or InActive
    conn_type text, -- File, Database, System...
	description text,

    UNIQUE (conn_name)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_system_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	system_type text, -- Prod , test
	description text,

    UNIQUE (system_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_map_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	map_type text, --default , custome
	description text,

    UNIQUE (map_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_file_mask
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	filemask text, --default , custome
	conversion text,

    UNIQUE (filemask)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_transaction_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	transaction_type text, --insert , update, upsert
	description text,

    UNIQUE (transaction_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_delimiter_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	delimiter_type text, --'|' , ',', '/'
	description text,

    UNIQUE (delimiter_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_line_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	line_type text, --'CRLF' , 'LF'
	description text,

    UNIQUE (line_type)
)
WITH (
    OIDS = FALSE
);

CREATE TABLE dim_field_type
(
    id serial PRIMARY KEY,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,

	field_type text, --'Auto' , 'numeric', 'text'
	description text,

    UNIQUE (field_type)
)
WITH (
    OIDS = FALSE
);



-- CREATE TABLE dim_job_type
-- (
--     id serial PRIMARY KEY,
--     sys_creation_date timestamp without time zone,
--     sys_update_date timestamp without time zone,
--     user_id text,

-- 	job_type text,
-- 	description text,

--     UNIQUE (job_type)
-- )
-- WITH (
--     OIDS = FALSE
-- );
