----=============================================
---- Description:  dim tables
----=============================================


----=============================================
--  insert statements for DIM tables
----=============================================


----=============================================
--   truncate statements
----=============================================

TRUNCATE TABLE dim_object_type;
TRUNCATE TABLE dim_connector;
TRUNCATE TABLE dim_system_type;

TRUNCATE TABLE dim_transaction_type;
TRUNCATE TABLE dim_delimiter_type;
TRUNCATE TABLE dim_line_type;
TRUNCATE TABLE dim_field_type;

----=============================================
--   Dim tables
----=============================================

-- insert into dim_object_type (object_type, description) values ('Model', 'Database Tables');
-- insert into dim_object_type (object_type, description) values ('Field', 'Database Fields');
insert into dim_object_type (object_type, description) values ('Organisation', 'Enterprise');
insert into dim_object_type (object_type, description) values ('Job', 'Scheduled Jobs');
insert into dim_object_type (object_type, description) values ('Connector', 'System Connector');
insert into dim_object_type (object_type, description) values ('Schedule', 'Job Schedule');

insert into dim_connector (conn_name, conn_usage, conn_logo_path, conn_status, conn_type, description)
    values ('File', 'Source', '/static/img/logo/file_system.jpg', 'Active', 'File', 'File connector');
insert into dim_connector (conn_name, conn_usage, conn_logo_path, conn_status , conn_type, description)
    values ('Salesforce', 'Destination', '/static/img/logo/salesforce.png', 'Active', 'System', 'Salesforce connector');
insert into dim_connector (conn_name, conn_usage, conn_logo_path, conn_status , conn_type, description)
    values ('AWS_S3', 'Source', '/static/img/logo/aws_s3.png', 'Active', 'File',  'AWS S3 connector');
insert into dim_connector (conn_name, conn_usage, conn_logo_path, conn_status , conn_type, description)
    values ('Postgres', 'Both', '/static/img/logo/postgresql.png', 'Active', 'Database', 'Postgres connector');
insert into dim_connector (conn_name, conn_usage, conn_logo_path, conn_status, conn_type, description)
    values ('Local', 'Source', '/static/img/logo/file_system.jpg', 'Active', 'File', 'Local File connector');

insert into dim_system_type (system_type, description) values ('Production', 'Production System');
insert into dim_system_type (system_type, description) values ('Sandbox', 'Sandbox / Test System');

insert into dim_map_type (map_type, description) values ('map', 'one to one mapping');
insert into dim_map_type (map_type, description) values ('constant', 'constant value');
insert into dim_map_type (map_type, description) values ('lookup', 'lookup from another object');
insert into dim_map_type (map_type, description) values ('ignore', 'ignore field');
insert into dim_map_type (map_type, description) values ('map_n_hook', 'one to one mapping with code hook');


insert into dim_file_mask (filemask, conversion) values ('DDMMYYYY', '%d%m%Y');
insert into dim_file_mask (filemask, conversion) values ('MMDDYYYY', '%m%d%Y');
insert into dim_file_mask (filemask, conversion) values ('YYYYMMDD', '%Y%d%m');
insert into dim_file_mask (filemask, conversion) values ('YYYYDDMM', '%Y%d%m');
insert into dim_file_mask (filemask, conversion) values ('None', 'None');

insert into  object(object_type, object_key, object_owner, effective_date)
values ('Connector', 'SidLocal', 'admin', now());

insert into  Connector(object_id, name, conn_name, conn_system_type)
select object_id, 'SidLocal', 'File', 'Production'
from object
where object_type = 'Connectors' and object_key = 'SidLocal'
and object_owner = 'admin'
;


insert into dim_transaction_type (transaction_type, description) values ('insert', 'insert');
insert into dim_transaction_type (transaction_type, description) values ('update', 'insert');
insert into dim_transaction_type (transaction_type, description) values ('upsert', 'insert');

insert into dim_delimiter_type (delimiter_type, description) values ('|', 'pipe');
insert into dim_delimiter_type (delimiter_type, description) values (',', 'comma');
insert into dim_delimiter_type (delimiter_type, description) values ('/', 'slash');
insert into dim_delimiter_type (delimiter_type, description) values ('#', 'hash');
insert into dim_delimiter_type (delimiter_type, description) values ('\\t', 'tab');

insert into dim_line_type (line_type, description) values ('CRLF', 'windows files');
insert into dim_line_type (line_type, description) values ('LF', 'unix files');

insert into dim_field_type (field_type, description) values ('Auto', 'Auto');
insert into dim_field_type (field_type, description) values ('Numeric', 'Numeric');
insert into dim_field_type (field_type, description) values ('Text', 'Text');
insert into dim_field_type (field_type, description) values ('Date', 'Date');
