CREATE USER debezium_business WITH REPLICATION PASSWORD ':debeziumpass';

CREATE ROLE business_owners_group;
GRANT business_owners_group TO debezium_business;

CREATE DATABASE domain_business OWNER business_owners_group;
