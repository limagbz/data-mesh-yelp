CREATE USER debezium_user WITH REPLICATION PASSWORD ':debeziumpass';

CREATE ROLE user_owners_group;
GRANT user_owners_group TO debezium_user;

CREATE DATABASE domain_user OWNER user_owners_group;
