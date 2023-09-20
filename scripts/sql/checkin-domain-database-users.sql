CREATE USER debezium_checkin WITH REPLICATION PASSWORD ':debeziumpass';

CREATE ROLE checkin_owners_group;
GRANT checkin_owners_group TO debezium_checkin;

CREATE DATABASE domain_checkin OWNER checkin_owners_group;
