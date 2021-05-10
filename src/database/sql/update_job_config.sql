----=============================================
--   update job config statements
--   a new field was introduced in v0.2 named model
----=============================================

alter table job_config add model text;

update job_config t1
set model = t2.dest_model
from (select distinct job_id, dest_model from model_map) t2
where t1.job_id = t2.job_id
and t1.rec_type = 'D'
;

update job_config t1
set model = t2.source_model
from (select distinct job_id, source_model from model_map) t2
where t1.job_id = t2.job_id
and t1.rec_type = 'S'
;


