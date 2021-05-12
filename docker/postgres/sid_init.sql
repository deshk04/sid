--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Debian 13.2-1.pgdg100+1)
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_aws_s3; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_aws_s3 (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    conn_object_id bigint,
    aws_access_key_id text,
    aws_secret_access_key text,
    bucket_name text,
    aws_region text,
    write_permission character(1)
);


ALTER TABLE public.auth_aws_s3 OWNER TO siduser;

--
-- Name: auth_aws_s3_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_aws_s3_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_aws_s3_id_seq OWNER TO siduser;

--
-- Name: auth_aws_s3_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_aws_s3_id_seq OWNED BY public.auth_aws_s3.id;


--
-- Name: auth_database; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_database (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    conn_object_id bigint,
    auth_username text,
    auth_password text,
    auth_database text,
    auth_host text
);


ALTER TABLE public.auth_database OWNER TO siduser;

--
-- Name: auth_database_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_database_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_database_id_seq OWNER TO siduser;

--
-- Name: auth_database_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_database_id_seq OWNED BY public.auth_database.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO siduser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO siduser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO siduser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO siduser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO siduser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO siduser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_salesforce; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_salesforce (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    conn_object_id bigint,
    auth_username text,
    auth_password text,
    auth_host text,
    security_token text,
    organisation_id text,
    consumer_key text,
    oauth_object_id text
);


ALTER TABLE public.auth_salesforce OWNER TO siduser;

--
-- Name: auth_salesforce_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_salesforce_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_salesforce_id_seq OWNER TO siduser;

--
-- Name: auth_salesforce_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_salesforce_id_seq OWNED BY public.auth_salesforce.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO siduser;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO siduser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO siduser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO siduser;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO siduser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO siduser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO siduser;

--
-- Name: connector; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.connector (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    object_id bigint,
    name text,
    conn_name text,
    conn_usage text,
    conn_system_type text
);


ALTER TABLE public.connector OWNER TO siduser;

--
-- Name: connector_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.connector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.connector_id_seq OWNER TO siduser;

--
-- Name: connector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.connector_id_seq OWNED BY public.connector.id;


--
-- Name: dim_connector; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_connector (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    conn_name text,
    conn_usage text,
    conn_logo_path text,
    conn_status text,
    conn_type text,
    description text
);


ALTER TABLE public.dim_connector OWNER TO siduser;

--
-- Name: dim_connector_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_connector_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_connector_id_seq OWNER TO siduser;

--
-- Name: dim_connector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_connector_id_seq OWNED BY public.dim_connector.id;


--
-- Name: dim_delimiter_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_delimiter_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    delimiter_type text,
    description text
);


ALTER TABLE public.dim_delimiter_type OWNER TO siduser;

--
-- Name: dim_delimiter_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_delimiter_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_delimiter_type_id_seq OWNER TO siduser;

--
-- Name: dim_delimiter_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_delimiter_type_id_seq OWNED BY public.dim_delimiter_type.id;


--
-- Name: dim_field_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_field_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    field_type text,
    description text
);


ALTER TABLE public.dim_field_type OWNER TO siduser;

--
-- Name: dim_field_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_field_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_field_type_id_seq OWNER TO siduser;

--
-- Name: dim_field_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_field_type_id_seq OWNED BY public.dim_field_type.id;


--
-- Name: dim_file_mask; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_file_mask (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    filemask text,
    conversion text
);


ALTER TABLE public.dim_file_mask OWNER TO siduser;

--
-- Name: dim_file_mask_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_file_mask_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_file_mask_id_seq OWNER TO siduser;

--
-- Name: dim_file_mask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_file_mask_id_seq OWNED BY public.dim_file_mask.id;


--
-- Name: dim_line_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_line_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    line_type text,
    description text
);


ALTER TABLE public.dim_line_type OWNER TO siduser;

--
-- Name: dim_line_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_line_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_line_type_id_seq OWNER TO siduser;

--
-- Name: dim_line_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_line_type_id_seq OWNED BY public.dim_line_type.id;


--
-- Name: dim_map_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_map_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    map_type text,
    description text
);


ALTER TABLE public.dim_map_type OWNER TO siduser;

--
-- Name: dim_map_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_map_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_map_type_id_seq OWNER TO siduser;

--
-- Name: dim_map_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_map_type_id_seq OWNED BY public.dim_map_type.id;


--
-- Name: dim_object_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_object_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    object_type text,
    description text
);


ALTER TABLE public.dim_object_type OWNER TO siduser;

--
-- Name: dim_object_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_object_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_object_type_id_seq OWNER TO siduser;

--
-- Name: dim_object_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_object_type_id_seq OWNED BY public.dim_object_type.id;


--
-- Name: dim_system_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_system_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    system_type text,
    description text
);


ALTER TABLE public.dim_system_type OWNER TO siduser;

--
-- Name: dim_system_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_system_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_system_type_id_seq OWNER TO siduser;

--
-- Name: dim_system_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_system_type_id_seq OWNED BY public.dim_system_type.id;


--
-- Name: dim_transaction_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dim_transaction_type (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    transaction_type text,
    description text
);


ALTER TABLE public.dim_transaction_type OWNER TO siduser;

--
-- Name: dim_transaction_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dim_transaction_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_transaction_type_id_seq OWNER TO siduser;

--
-- Name: dim_transaction_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dim_transaction_type_id_seq OWNED BY public.dim_transaction_type.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO siduser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO siduser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO siduser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO siduser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO siduser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO siduser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO siduser;

--
-- Name: dmodels; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.dmodels (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    conn_object_id bigint,
    name text,
    label text,
    readable text,
    writeable text
);


ALTER TABLE public.dmodels OWNER TO siduser;

--
-- Name: dmodels_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.dmodels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dmodels_id_seq OWNER TO siduser;

--
-- Name: dmodels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.dmodels_id_seq OWNED BY public.dmodels.id;


--
-- Name: fields; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.fields (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    model_id bigint,
    field_name text,
    field_type text,
    field_length text,
    field_format text,
    label text,
    primary_key character(1),
    choices text,
    nullable character(1)
);


ALTER TABLE public.fields OWNER TO siduser;

--
-- Name: fields_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fields_id_seq OWNER TO siduser;

--
-- Name: fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.fields_id_seq OWNED BY public.fields.id;


--
-- Name: job_config; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.job_config (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    job_id bigint,
    rec_type character(1) NOT NULL,
    conn_object_id bigint,
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
    transaction_type text
);


ALTER TABLE public.job_config OWNER TO siduser;

--
-- Name: job_config_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.job_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.job_config_id_seq OWNER TO siduser;

--
-- Name: job_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.job_config_id_seq OWNED BY public.job_config.id;


--
-- Name: job_distribution; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.job_distribution (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    job_id bigint,
    file_type text,
    email_flag character(1) DEFAULT 'N'::bpchar,
    tolist text,
    cclist text,
    bcclist text
);


ALTER TABLE public.job_distribution OWNER TO siduser;

--
-- Name: job_distribution_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.job_distribution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.job_distribution_id_seq OWNER TO siduser;

--
-- Name: job_distribution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.job_distribution_id_seq OWNED BY public.job_distribution.id;


--
-- Name: jobrun_details; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.jobrun_details (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    jobrun_id bigint,
    record_number integer,
    record_key text,
    record_value text,
    status_code text,
    status_message text,
    orig_record text,
    processed_record text
);


ALTER TABLE public.jobrun_details OWNER TO siduser;

--
-- Name: jobrun_details_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.jobrun_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobrun_details_id_seq OWNER TO siduser;

--
-- Name: jobrun_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.jobrun_details_id_seq OWNED BY public.jobrun_details.id;


--
-- Name: jobrun_log; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.jobrun_log (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    job_id bigint,
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
);


ALTER TABLE public.jobrun_log OWNER TO siduser;

--
-- Name: jobrun_log_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.jobrun_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobrun_log_id_seq OWNER TO siduser;

--
-- Name: jobrun_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.jobrun_log_id_seq OWNED BY public.jobrun_log.id;


--
-- Name: jobs; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.jobs (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    job_id bigint,
    job_name text,
    run_type character(1),
    parallel_count integer
);


ALTER TABLE public.jobs OWNER TO siduser;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.jobs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_id_seq OWNER TO siduser;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.jobs_id_seq OWNED BY public.jobs.id;


--
-- Name: model_map; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.model_map (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    job_id bigint NOT NULL,
    source_model text,
    source_field text NOT NULL,
    map_type text,
    map_value text,
    lookup_model text,
    lookup_join_field text,
    lookup_return_field text,
    dest_model text NOT NULL,
    dest_field text,
    errormsg text
);


ALTER TABLE public.model_map OWNER TO siduser;

--
-- Name: model_map_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.model_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.model_map_id_seq OWNER TO siduser;

--
-- Name: model_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.model_map_id_seq OWNED BY public.model_map.id;


--
-- Name: object; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.object (
    object_id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    object_type text,
    object_key text,
    object_owner text,
    effective_date date,
    expiration_date date
);


ALTER TABLE public.object OWNER TO siduser;

--
-- Name: object_object_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.object_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.object_object_id_seq OWNER TO siduser;

--
-- Name: object_object_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.object_object_id_seq OWNED BY public.object.object_id;


--
-- Name: schedule; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.schedule (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    schedule_id bigint,
    schedule_type text,
    schedule_name text NOT NULL,
    schedule_owner text NOT NULL,
    rerun_flag character(1),
    frequency text NOT NULL,
    day_of_week text,
    month text,
    day_of_month text,
    hours text,
    minutes text,
    comment text
);


ALTER TABLE public.schedule OWNER TO siduser;

--
-- Name: schedule_config; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.schedule_config (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    schedule_id bigint,
    job_sequence integer,
    job_id bigint,
    active_flag character(1)
);


ALTER TABLE public.schedule_config OWNER TO siduser;

--
-- Name: schedule_config_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.schedule_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_config_id_seq OWNER TO siduser;

--
-- Name: schedule_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.schedule_config_id_seq OWNED BY public.schedule_config.id;


--
-- Name: schedule_distribution; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.schedule_distribution (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    schedule_id bigint,
    email_flag character(1) DEFAULT 'N'::bpchar,
    tolist text,
    cclist text,
    bcclist text
);


ALTER TABLE public.schedule_distribution OWNER TO siduser;

--
-- Name: schedule_distribution_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.schedule_distribution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_distribution_id_seq OWNER TO siduser;

--
-- Name: schedule_distribution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.schedule_distribution_id_seq OWNED BY public.schedule_distribution.id;


--
-- Name: schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_id_seq OWNER TO siduser;

--
-- Name: schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.schedule_id_seq OWNED BY public.schedule.id;


--
-- Name: schedule_log; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.schedule_log (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    schedule_id bigint,
    run_date date,
    message text,
    status text
);


ALTER TABLE public.schedule_log OWNER TO siduser;

--
-- Name: schedule_log_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.schedule_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.schedule_log_id_seq OWNER TO siduser;

--
-- Name: schedule_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.schedule_log_id_seq OWNED BY public.schedule_log.id;


--
-- Name: sid_settings; Type: TABLE; Schema: public; Owner: siduser
--

CREATE TABLE public.sid_settings (
    id integer NOT NULL,
    sys_creation_date timestamp without time zone,
    sys_update_date timestamp without time zone,
    user_id text,
    object_owner text,
    key text,
    value text
);


ALTER TABLE public.sid_settings OWNER TO siduser;

--
-- Name: sid_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: siduser
--

CREATE SEQUENCE public.sid_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sid_settings_id_seq OWNER TO siduser;

--
-- Name: sid_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: siduser
--

ALTER SEQUENCE public.sid_settings_id_seq OWNED BY public.sid_settings.id;


--
-- Name: auth_aws_s3 id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_aws_s3 ALTER COLUMN id SET DEFAULT nextval('public.auth_aws_s3_id_seq'::regclass);


--
-- Name: auth_database id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_database ALTER COLUMN id SET DEFAULT nextval('public.auth_database_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_salesforce id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_salesforce ALTER COLUMN id SET DEFAULT nextval('public.auth_salesforce_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: connector id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector ALTER COLUMN id SET DEFAULT nextval('public.connector_id_seq'::regclass);


--
-- Name: dim_connector id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_connector ALTER COLUMN id SET DEFAULT nextval('public.dim_connector_id_seq'::regclass);


--
-- Name: dim_delimiter_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_delimiter_type ALTER COLUMN id SET DEFAULT nextval('public.dim_delimiter_type_id_seq'::regclass);


--
-- Name: dim_field_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_field_type ALTER COLUMN id SET DEFAULT nextval('public.dim_field_type_id_seq'::regclass);


--
-- Name: dim_file_mask id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_file_mask ALTER COLUMN id SET DEFAULT nextval('public.dim_file_mask_id_seq'::regclass);


--
-- Name: dim_line_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_line_type ALTER COLUMN id SET DEFAULT nextval('public.dim_line_type_id_seq'::regclass);


--
-- Name: dim_map_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_map_type ALTER COLUMN id SET DEFAULT nextval('public.dim_map_type_id_seq'::regclass);


--
-- Name: dim_object_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_object_type ALTER COLUMN id SET DEFAULT nextval('public.dim_object_type_id_seq'::regclass);


--
-- Name: dim_system_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_system_type ALTER COLUMN id SET DEFAULT nextval('public.dim_system_type_id_seq'::regclass);


--
-- Name: dim_transaction_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_transaction_type ALTER COLUMN id SET DEFAULT nextval('public.dim_transaction_type_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: dmodels id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dmodels ALTER COLUMN id SET DEFAULT nextval('public.dmodels_id_seq'::regclass);


--
-- Name: fields id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.fields ALTER COLUMN id SET DEFAULT nextval('public.fields_id_seq'::regclass);


--
-- Name: job_config id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_config ALTER COLUMN id SET DEFAULT nextval('public.job_config_id_seq'::regclass);


--
-- Name: job_distribution id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_distribution ALTER COLUMN id SET DEFAULT nextval('public.job_distribution_id_seq'::regclass);


--
-- Name: jobrun_details id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_details ALTER COLUMN id SET DEFAULT nextval('public.jobrun_details_id_seq'::regclass);


--
-- Name: jobrun_log id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_log ALTER COLUMN id SET DEFAULT nextval('public.jobrun_log_id_seq'::regclass);


--
-- Name: jobs id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id SET DEFAULT nextval('public.jobs_id_seq'::regclass);


--
-- Name: model_map id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.model_map ALTER COLUMN id SET DEFAULT nextval('public.model_map_id_seq'::regclass);


--
-- Name: object object_id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.object ALTER COLUMN object_id SET DEFAULT nextval('public.object_object_id_seq'::regclass);


--
-- Name: schedule id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule ALTER COLUMN id SET DEFAULT nextval('public.schedule_id_seq'::regclass);


--
-- Name: schedule_config id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_config ALTER COLUMN id SET DEFAULT nextval('public.schedule_config_id_seq'::regclass);


--
-- Name: schedule_distribution id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_distribution ALTER COLUMN id SET DEFAULT nextval('public.schedule_distribution_id_seq'::regclass);


--
-- Name: schedule_log id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_log ALTER COLUMN id SET DEFAULT nextval('public.schedule_log_id_seq'::regclass);


--
-- Name: sid_settings id; Type: DEFAULT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.sid_settings ALTER COLUMN id SET DEFAULT nextval('public.sid_settings_id_seq'::regclass);


--
-- Data for Name: auth_aws_s3; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_aws_s3 (id, sys_creation_date, sys_update_date, user_id, conn_object_id, aws_access_key_id, aws_secret_access_key, bucket_name, aws_region, write_permission) FROM stdin;
\.


--
-- Data for Name: auth_database; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_database (id, sys_creation_date, sys_update_date, user_id, conn_object_id, auth_username, auth_password, auth_database, auth_host) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
\.


--
-- Data for Name: auth_salesforce; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_salesforce (id, sys_creation_date, sys_update_date, user_id, conn_object_id, auth_username, auth_password, auth_host, security_token, organisation_id, consumer_key, oauth_object_id) FROM stdin;
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$xKaDqpm87JmV$Z2C1PtwUMlPe/kkC6fXTenVx8iGvECAe5WEYS07RVyE=	2021-05-12 19:55:09+10	t	admin	admin		admin@sid.local	t	t	2021-05-12 19:55:01+10
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- Data for Name: connector; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.connector (id, sys_creation_date, sys_update_date, user_id, object_id, name, conn_name, conn_usage, conn_system_type) FROM stdin;
\.


--
-- Data for Name: dim_connector; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_connector (id, sys_creation_date, sys_update_date, user_id, conn_name, conn_usage, conn_logo_path, conn_status, conn_type, description) FROM stdin;
1	\N	\N	\N	File	Source	/static/img/logo/file_system.jpg	Active	File	File connector
2	\N	\N	\N	Salesforce	Destination	/static/img/logo/salesforce.png	Active	System	Salesforce connector
3	\N	\N	\N	AWS_S3	Source	/static/img/logo/aws_s3.png	Active	File	AWS S3 connector
4	\N	\N	\N	Postgres	Both	/static/img/logo/postgresql.png	Active	Database	Postgres connector
5	\N	\N	\N	Local	Source	/static/img/logo/file_system.jpg	Active	File	Local File connector
\.


--
-- Data for Name: dim_delimiter_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_delimiter_type (id, sys_creation_date, sys_update_date, user_id, delimiter_type, description) FROM stdin;
1	\N	\N	\N	|	pipe
2	\N	\N	\N	,	comma
3	\N	\N	\N	/	slash
4	\N	\N	\N	#	hash
5	\N	\N	\N	\\\\t	tab
\.


--
-- Data for Name: dim_field_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_field_type (id, sys_creation_date, sys_update_date, user_id, field_type, description) FROM stdin;
1	\N	\N	\N	Auto	Auto
2	\N	\N	\N	Numeric	Numeric
3	\N	\N	\N	Text	Text
4	\N	\N	\N	Date	Date
\.


--
-- Data for Name: dim_file_mask; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_file_mask (id, sys_creation_date, sys_update_date, user_id, filemask, conversion) FROM stdin;
1	\N	\N	\N	DDMMYYYY	%d%m%Y
2	\N	\N	\N	MMDDYYYY	%m%d%Y
3	\N	\N	\N	YYYYMMDD	%Y%d%m
4	\N	\N	\N	YYYYDDMM	%Y%d%m
5	\N	\N	\N	None	None
\.


--
-- Data for Name: dim_line_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_line_type (id, sys_creation_date, sys_update_date, user_id, line_type, description) FROM stdin;
1	\N	\N	\N	CRLF	windows files
2	\N	\N	\N	LF	unix files
\.


--
-- Data for Name: dim_map_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_map_type (id, sys_creation_date, sys_update_date, user_id, map_type, description) FROM stdin;
1	\N	\N	\N	map	one to one mapping
2	\N	\N	\N	constant	constant value
3	\N	\N	\N	lookup	lookup from another object
4	\N	\N	\N	ignore	ignore field
5	\N	\N	\N	map_n_hook	one to one mapping with code hook
\.


--
-- Data for Name: dim_object_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_object_type (id, sys_creation_date, sys_update_date, user_id, object_type, description) FROM stdin;
1	\N	\N	\N	Organisation	Enterprise
2	\N	\N	\N	Job	Scheduled Jobs
3	\N	\N	\N	Connector	System Connector
4	\N	\N	\N	Schedule	Job Schedule
\.


--
-- Data for Name: dim_system_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_system_type (id, sys_creation_date, sys_update_date, user_id, system_type, description) FROM stdin;
1	\N	\N	\N	Production	Production System
2	\N	\N	\N	Sandbox	Sandbox / Test System
\.


--
-- Data for Name: dim_transaction_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dim_transaction_type (id, sys_creation_date, sys_update_date, user_id, transaction_type, description) FROM stdin;
1	\N	\N	\N	insert	insert
2	\N	\N	\N	update	insert
3	\N	\N	\N	upsert	insert
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2021-05-12 19:56:59.283806+10	1	admin	2	[{"changed": {"fields": ["First name", "Email address"]}}]	4	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	authtoken	token
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-05-12 19:53:04.232664+10
2	auth	0001_initial	2021-05-12 19:53:04.258799+10
3	admin	0001_initial	2021-05-12 19:53:04.292339+10
4	admin	0002_logentry_remove_auto_add	2021-05-12 19:53:04.303368+10
5	admin	0003_logentry_add_action_flag_choices	2021-05-12 19:53:04.309551+10
6	contenttypes	0002_remove_content_type_name	2021-05-12 19:53:04.321947+10
7	auth	0002_alter_permission_name_max_length	2021-05-12 19:53:04.329369+10
8	auth	0003_alter_user_email_max_length	2021-05-12 19:53:04.336642+10
9	auth	0004_alter_user_username_opts	2021-05-12 19:53:04.342889+10
10	auth	0005_alter_user_last_login_null	2021-05-12 19:53:04.349378+10
11	auth	0006_require_contenttypes_0002	2021-05-12 19:53:04.351529+10
12	auth	0007_alter_validators_add_error_messages	2021-05-12 19:53:04.358051+10
13	auth	0008_alter_user_username_max_length	2021-05-12 19:53:04.367258+10
14	auth	0009_alter_user_last_name_max_length	2021-05-12 19:53:04.375725+10
15	auth	0010_alter_group_name_max_length	2021-05-12 19:53:04.383429+10
16	auth	0011_update_proxy_permissions	2021-05-12 19:53:04.38979+10
17	auth	0012_alter_user_first_name_max_length	2021-05-12 19:53:04.396268+10
18	authtoken	0001_initial	2021-05-12 19:53:04.405898+10
19	authtoken	0002_auto_20160226_1747	2021-05-12 19:53:04.432374+10
20	sessions	0001_initial	2021-05-12 19:53:04.439023+10
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
vhs5w8487qpa3ndn30jjr30lnlups0m0	.eJxVjDsOwyAQBe9CHSHAfEzK9D4D2mUhOIlAMnYV5e4RkoukfTPz3izAsZdw9LSFldiVSXb53RDiM9UB6AH13nhsdd9W5EPhJ-18aZRet9P9OyjQy6jFhEQASpC2lGFydpbeKqujcS46AUkoj4ggddRqRmlEViZL551WZmKfL-oKN14:1lgla9:WLWFVfM-eQh6lk84TLtUZ_C3QJ-Zdmv4O7zOcaOMxI8	2021-05-26 19:55:09.277492+10
\.


--
-- Data for Name: dmodels; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.dmodels (id, sys_creation_date, sys_update_date, user_id, conn_object_id, name, label, readable, writeable) FROM stdin;
\.


--
-- Data for Name: fields; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.fields (id, sys_creation_date, sys_update_date, user_id, model_id, field_name, field_type, field_length, field_format, label, primary_key, choices, nullable) FROM stdin;
\.


--
-- Data for Name: job_config; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.job_config (id, sys_creation_date, sys_update_date, user_id, job_id, rec_type, conn_object_id, filepath, filestartwith, fileendwith, filemask, delimiter, encoding, lineterminator, archivepath, key_field, bulk_count, query, transaction_type) FROM stdin;
\.


--
-- Data for Name: job_distribution; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.job_distribution (id, sys_creation_date, sys_update_date, user_id, job_id, file_type, email_flag, tolist, cclist, bcclist) FROM stdin;
\.


--
-- Data for Name: jobrun_details; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.jobrun_details (id, sys_creation_date, sys_update_date, user_id, jobrun_id, record_number, record_key, record_value, status_code, status_message, orig_record, processed_record) FROM stdin;
\.


--
-- Data for Name: jobrun_log; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.jobrun_log (id, sys_creation_date, sys_update_date, user_id, job_id, filename, file_date, run_date, message, status, total_count, success_count, failure_count, warning_count, schedule_id, schedulelog_id) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.jobs (id, sys_creation_date, sys_update_date, user_id, job_id, job_name, run_type, parallel_count) FROM stdin;
\.


--
-- Data for Name: model_map; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.model_map (id, sys_creation_date, sys_update_date, user_id, job_id, source_model, source_field, map_type, map_value, lookup_model, lookup_join_field, lookup_return_field, dest_model, dest_field, errormsg) FROM stdin;
\.


--
-- Data for Name: object; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.object (object_id, sys_creation_date, sys_update_date, user_id, object_type, object_key, object_owner, effective_date, expiration_date) FROM stdin;
1	\N	\N	\N	Connector	SidLocal	admin	2021-05-12	\N
\.


--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.schedule (id, sys_creation_date, sys_update_date, user_id, schedule_id, schedule_type, schedule_name, schedule_owner, rerun_flag, frequency, day_of_week, month, day_of_month, hours, minutes, comment) FROM stdin;
\.


--
-- Data for Name: schedule_config; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.schedule_config (id, sys_creation_date, sys_update_date, user_id, schedule_id, job_sequence, job_id, active_flag) FROM stdin;
\.


--
-- Data for Name: schedule_distribution; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.schedule_distribution (id, sys_creation_date, sys_update_date, user_id, schedule_id, email_flag, tolist, cclist, bcclist) FROM stdin;
\.


--
-- Data for Name: schedule_log; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.schedule_log (id, sys_creation_date, sys_update_date, user_id, schedule_id, run_date, message, status) FROM stdin;
\.


--
-- Data for Name: sid_settings; Type: TABLE DATA; Schema: public; Owner: siduser
--

COPY public.sid_settings (id, sys_creation_date, sys_update_date, user_id, object_owner, key, value) FROM stdin;
1	2021-05-12 19:44:07.289483	\N	system	system	SYSTEM_USER	system
2	2021-05-12 19:44:07.291906	\N	system	system	SID_ADMIN	admin
3	2021-05-12 19:44:07.293302	\N	system	system	BULK_COUNT	200
4	2021-05-12 19:44:07.294676	\N	system	system	SCHEDULE_EMAIL	N
5	2021-05-12 19:44:07.296106	\N	system	system	JOB_EMAIL	N
6	2021-05-12 19:44:07.297565	\N	system	system	EMAIL_SUBJECT_PREFIX	[SID]
7	2021-05-12 19:44:07.298918	\N	system	system	EMAIL_FROM	noreply@localhost.com
8	2021-05-12 19:44:07.300221	\N	system	system	EMAIL_SUPPORT	noreply@localhost.com
9	2021-05-12 19:44:07.301574	\N	system	system	SFOPTIMIZE	Y
10	2021-05-12 19:44:07.302819	\N	system	system	SFLOOKUP_FILESIZE	0
11	2021-05-12 19:44:07.304186	\N	system	system	SFLOOKUP_RECHECK	N
12	2021-05-12 19:44:07.305582	\N	system	system	SCHEDULE_PARALLEL	N
13	2021-05-12 19:44:07.30691	\N	system	system	PARALLEL_COUNT	1
\.


--
-- Name: auth_aws_s3_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_aws_s3_id_seq', 1, false);


--
-- Name: auth_database_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_database_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 28, true);


--
-- Name: auth_salesforce_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_salesforce_id_seq', 1, false);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: connector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.connector_id_seq', 1, false);


--
-- Name: dim_connector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_connector_id_seq', 5, true);


--
-- Name: dim_delimiter_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_delimiter_type_id_seq', 5, true);


--
-- Name: dim_field_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_field_type_id_seq', 4, true);


--
-- Name: dim_file_mask_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_file_mask_id_seq', 5, true);


--
-- Name: dim_line_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_line_type_id_seq', 2, true);


--
-- Name: dim_map_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_map_type_id_seq', 5, true);


--
-- Name: dim_object_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_object_type_id_seq', 4, true);


--
-- Name: dim_system_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_system_type_id_seq', 2, true);


--
-- Name: dim_transaction_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dim_transaction_type_id_seq', 3, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 7, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: dmodels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.dmodels_id_seq', 1, false);


--
-- Name: fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.fields_id_seq', 1, false);


--
-- Name: job_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.job_config_id_seq', 1, false);


--
-- Name: job_distribution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.job_distribution_id_seq', 1, false);


--
-- Name: jobrun_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.jobrun_details_id_seq', 1, false);


--
-- Name: jobrun_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.jobrun_log_id_seq', 1, false);


--
-- Name: jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.jobs_id_seq', 1, false);


--
-- Name: model_map_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.model_map_id_seq', 1, false);


--
-- Name: object_object_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.object_object_id_seq', 1, true);


--
-- Name: schedule_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.schedule_config_id_seq', 1, false);


--
-- Name: schedule_distribution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.schedule_distribution_id_seq', 1, false);


--
-- Name: schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.schedule_id_seq', 1, false);


--
-- Name: schedule_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.schedule_log_id_seq', 1, false);


--
-- Name: sid_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: siduser
--

SELECT pg_catalog.setval('public.sid_settings_id_seq', 13, true);


--
-- Name: auth_aws_s3 auth_aws_s3_conn_object_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_aws_s3
    ADD CONSTRAINT auth_aws_s3_conn_object_id_key UNIQUE (conn_object_id);


--
-- Name: auth_aws_s3 auth_aws_s3_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_aws_s3
    ADD CONSTRAINT auth_aws_s3_pkey PRIMARY KEY (id);


--
-- Name: auth_database auth_database_conn_object_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_database
    ADD CONSTRAINT auth_database_conn_object_id_key UNIQUE (conn_object_id);


--
-- Name: auth_database auth_database_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_database
    ADD CONSTRAINT auth_database_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_salesforce auth_salesforce_conn_object_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_salesforce
    ADD CONSTRAINT auth_salesforce_conn_object_id_key UNIQUE (conn_object_id);


--
-- Name: auth_salesforce auth_salesforce_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_salesforce
    ADD CONSTRAINT auth_salesforce_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: connector connector_object_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector
    ADD CONSTRAINT connector_object_id_key UNIQUE (object_id);


--
-- Name: connector connector_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector
    ADD CONSTRAINT connector_pkey PRIMARY KEY (id);


--
-- Name: dim_connector dim_connector_conn_name_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_connector
    ADD CONSTRAINT dim_connector_conn_name_key UNIQUE (conn_name);


--
-- Name: dim_connector dim_connector_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_connector
    ADD CONSTRAINT dim_connector_pkey PRIMARY KEY (id);


--
-- Name: dim_delimiter_type dim_delimiter_type_delimiter_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_delimiter_type
    ADD CONSTRAINT dim_delimiter_type_delimiter_type_key UNIQUE (delimiter_type);


--
-- Name: dim_delimiter_type dim_delimiter_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_delimiter_type
    ADD CONSTRAINT dim_delimiter_type_pkey PRIMARY KEY (id);


--
-- Name: dim_field_type dim_field_type_field_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_field_type
    ADD CONSTRAINT dim_field_type_field_type_key UNIQUE (field_type);


--
-- Name: dim_field_type dim_field_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_field_type
    ADD CONSTRAINT dim_field_type_pkey PRIMARY KEY (id);


--
-- Name: dim_file_mask dim_file_mask_filemask_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_file_mask
    ADD CONSTRAINT dim_file_mask_filemask_key UNIQUE (filemask);


--
-- Name: dim_file_mask dim_file_mask_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_file_mask
    ADD CONSTRAINT dim_file_mask_pkey PRIMARY KEY (id);


--
-- Name: dim_line_type dim_line_type_line_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_line_type
    ADD CONSTRAINT dim_line_type_line_type_key UNIQUE (line_type);


--
-- Name: dim_line_type dim_line_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_line_type
    ADD CONSTRAINT dim_line_type_pkey PRIMARY KEY (id);


--
-- Name: dim_map_type dim_map_type_map_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_map_type
    ADD CONSTRAINT dim_map_type_map_type_key UNIQUE (map_type);


--
-- Name: dim_map_type dim_map_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_map_type
    ADD CONSTRAINT dim_map_type_pkey PRIMARY KEY (id);


--
-- Name: dim_object_type dim_object_type_object_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_object_type
    ADD CONSTRAINT dim_object_type_object_type_key UNIQUE (object_type);


--
-- Name: dim_object_type dim_object_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_object_type
    ADD CONSTRAINT dim_object_type_pkey PRIMARY KEY (id);


--
-- Name: dim_system_type dim_system_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_system_type
    ADD CONSTRAINT dim_system_type_pkey PRIMARY KEY (id);


--
-- Name: dim_system_type dim_system_type_system_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_system_type
    ADD CONSTRAINT dim_system_type_system_type_key UNIQUE (system_type);


--
-- Name: dim_transaction_type dim_transaction_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_transaction_type
    ADD CONSTRAINT dim_transaction_type_pkey PRIMARY KEY (id);


--
-- Name: dim_transaction_type dim_transaction_type_transaction_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dim_transaction_type
    ADD CONSTRAINT dim_transaction_type_transaction_type_key UNIQUE (transaction_type);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: dmodels dmodels_conn_object_id_name_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dmodels
    ADD CONSTRAINT dmodels_conn_object_id_name_key UNIQUE (conn_object_id, name);


--
-- Name: dmodels dmodels_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dmodels
    ADD CONSTRAINT dmodels_pkey PRIMARY KEY (id);


--
-- Name: fields fields_model_id_field_name_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_model_id_field_name_key UNIQUE (model_id, field_name);


--
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- Name: job_config job_config_job_id_rec_type_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_config
    ADD CONSTRAINT job_config_job_id_rec_type_key UNIQUE (job_id, rec_type);


--
-- Name: job_config job_config_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_config
    ADD CONSTRAINT job_config_pkey PRIMARY KEY (id);


--
-- Name: job_distribution job_distribution_job_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_distribution
    ADD CONSTRAINT job_distribution_job_id_key UNIQUE (job_id);


--
-- Name: job_distribution job_distribution_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_distribution
    ADD CONSTRAINT job_distribution_pkey PRIMARY KEY (id);


--
-- Name: jobrun_details jobrun_details_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_details
    ADD CONSTRAINT jobrun_details_pkey PRIMARY KEY (id);


--
-- Name: jobrun_log jobrun_log_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_log
    ADD CONSTRAINT jobrun_log_pkey PRIMARY KEY (id);


--
-- Name: jobs jobs_job_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_job_id_key UNIQUE (job_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: model_map model_map_job_id_source_field_map_type_dest_field_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.model_map
    ADD CONSTRAINT model_map_job_id_source_field_map_type_dest_field_key UNIQUE (job_id, source_field, map_type, dest_field);


--
-- Name: model_map model_map_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.model_map
    ADD CONSTRAINT model_map_pkey PRIMARY KEY (id);


--
-- Name: object object_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_pkey PRIMARY KEY (object_id);


--
-- Name: schedule_config schedule_config_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_config
    ADD CONSTRAINT schedule_config_pkey PRIMARY KEY (id);


--
-- Name: schedule_distribution schedule_distribution_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_distribution
    ADD CONSTRAINT schedule_distribution_pkey PRIMARY KEY (id);


--
-- Name: schedule_distribution schedule_distribution_schedule_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_distribution
    ADD CONSTRAINT schedule_distribution_schedule_id_key UNIQUE (schedule_id);


--
-- Name: schedule_log schedule_log_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_log
    ADD CONSTRAINT schedule_log_pkey PRIMARY KEY (id);


--
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (id);


--
-- Name: schedule schedule_schedule_id_key; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_schedule_id_key UNIQUE (schedule_id);


--
-- Name: sid_settings sid_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.sid_settings
    ADD CONSTRAINT sid_settings_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: siduser
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_aws_s3 auth_aws_s3_conn_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_aws_s3
    ADD CONSTRAINT auth_aws_s3_conn_object_id_fkey FOREIGN KEY (conn_object_id) REFERENCES public.connector(object_id);


--
-- Name: auth_database auth_database_conn_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_database
    ADD CONSTRAINT auth_database_conn_object_id_fkey FOREIGN KEY (conn_object_id) REFERENCES public.connector(object_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_salesforce auth_salesforce_conn_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_salesforce
    ADD CONSTRAINT auth_salesforce_conn_object_id_fkey FOREIGN KEY (conn_object_id) REFERENCES public.connector(object_id);


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: connector connector_conn_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector
    ADD CONSTRAINT connector_conn_name_fkey FOREIGN KEY (conn_name) REFERENCES public.dim_connector(conn_name);


--
-- Name: connector connector_conn_system_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector
    ADD CONSTRAINT connector_conn_system_type_fkey FOREIGN KEY (conn_system_type) REFERENCES public.dim_system_type(system_type);


--
-- Name: connector connector_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.connector
    ADD CONSTRAINT connector_object_id_fkey FOREIGN KEY (object_id) REFERENCES public.object(object_id);


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dmodels dmodels_conn_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.dmodels
    ADD CONSTRAINT dmodels_conn_object_id_fkey FOREIGN KEY (conn_object_id) REFERENCES public.connector(object_id);


--
-- Name: fields fields_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.dmodels(id);


--
-- Name: job_config job_config_conn_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_config
    ADD CONSTRAINT job_config_conn_object_id_fkey FOREIGN KEY (conn_object_id) REFERENCES public.connector(object_id);


--
-- Name: job_config job_config_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.job_config
    ADD CONSTRAINT job_config_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id);


--
-- Name: jobrun_details jobrun_details_jobrun_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_details
    ADD CONSTRAINT jobrun_details_jobrun_id_fkey FOREIGN KEY (jobrun_id) REFERENCES public.jobrun_log(id);


--
-- Name: jobrun_log jobrun_log_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobrun_log
    ADD CONSTRAINT jobrun_log_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id);


--
-- Name: jobs jobs_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.object(object_id);


--
-- Name: model_map model_map_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.model_map
    ADD CONSTRAINT model_map_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id);


--
-- Name: model_map model_map_map_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.model_map
    ADD CONSTRAINT model_map_map_type_fkey FOREIGN KEY (map_type) REFERENCES public.dim_map_type(map_type);


--
-- Name: schedule_config schedule_config_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_config
    ADD CONSTRAINT schedule_config_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedule(schedule_id);


--
-- Name: schedule_distribution schedule_distribution_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_distribution
    ADD CONSTRAINT schedule_distribution_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedule(schedule_id);


--
-- Name: schedule_log schedule_log_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: siduser
--

ALTER TABLE ONLY public.schedule_log
    ADD CONSTRAINT schedule_log_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES public.schedule(schedule_id);


--
-- PostgreSQL database dump complete
--

