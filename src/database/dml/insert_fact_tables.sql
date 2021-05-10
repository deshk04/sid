----=============================================
--   truncate statements
----=============================================

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SYSTEM_USER', 'system');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SID_ADMIN', 'admin');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'BULK_COUNT', '200');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SCHEDULE_EMAIL', 'N');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'JOB_EMAIL', 'N');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'EMAIL_SUBJECT_PREFIX', '[SID]');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'EMAIL_FROM', 'noreply@localhost.com');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'EMAIL_SUPPORT', 'noreply@localhost.com');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SFOPTIMIZE', 'Y');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SFLOOKUP_FILESIZE', '0');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SFLOOKUP_RECHECK', 'N');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'SCHEDULE_PARALLEL', 'N');

insert into  sid_settings(sys_creation_date, user_id, object_owner, key, value)
values (now(), 'system',  'system', 'PARALLEL_COUNT', '1');
