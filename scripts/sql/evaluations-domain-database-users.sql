CREATE USER debezium_evaluations WITH REPLICATION PASSWORD ':debeziumpass';

CREATE ROLE evaluations_owners_group;
GRANT evaluations_owners_group TO debezium_evaluations;

CREATE DATABASE domain_evaluations OWNER evaluations_owners_group;
