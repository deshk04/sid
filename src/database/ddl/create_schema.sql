----=============================================
---- Description:  create statement
----=============================================


----=============================================
--  Create database
----=============================================
-- change owner of the location to postgres user
DROP DATABASE sidmain;

CREATE DATABASE sidmain
    WITH
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE sidmain
    IS 'main sid database';


CREATE USER siduser WITH ENCRYPTED PASSWORD 'M1ll4murr4';
GRANT ALL PRIVILEGES ON DATABASE sidmain TO siduser;

\connect sidmain

DROP SCHEMA work;

CREATE SCHEMA work;

CREATE DATABASE logs
    WITH
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE logs
    IS 'logs database';
