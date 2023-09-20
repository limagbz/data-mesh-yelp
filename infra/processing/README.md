# Processing

1. [Overview](#overview)
1. [Deployment Guide](#deployment-guide)
1. [FAQ](#faq)
1. [Further Reading](#further-reading)

## Overview

This namespace contains all the infrastructure required to process data from ingestion to the development
of data products. This includes a [Kafka](https://kafka.apache.org/documentation/#gettingStarted) and
[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html#kafka-connect) used to transfer
operational data from PostgreSQL to a MinIO tenant via change data capture (using
[Debezium](https://debezium.io/documentation/)), [Trino](https://trino.io/) and
[Hive Metastore](https://cwiki.apache.org/confluence/display/hive/design#Design-Metastore) to query data
directly from MinIO. And also [dbt](https://docs.getdbt.com/) to be able to process all the data into products.

## Deployment Guide

> [!WARNING]
> Before deploying any resource on this folder, please create the namespace by running:
> `kubectl apply -f infra/processing/namespace.yaml`

### Kafka (and Kafka Connect)

To deploy Kafka we are going to use the [Strimzi Operator](https://strimzi.io/). This operators provide ways
to deploy not only Kafka but many related resources such as Kafka Exporter, Mirrormake, Bridge and so on.
For this lab we are only going to need Kafka Connect. To deploy the operator run:

```shell
helm install -f infra/processing/kafka/values.yaml kafka-operator infra/processing/kafka/helm -n processing
```

With the operator deployed we now deploy the Kafka Cluster and required resources such as Zookeeper (for
brokers and consumers coordination), and Exporter (to send metrics to Prometheus).

```shell
kubectl apply -f infra/processing/kafka/kafka-cluster.yaml
```

With the cluster working we need to configure both the [PostgreSQL Source](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
and [S3 Sink](https://docs.confluent.io/kafka-connectors/s3-sink/current/overview.html#) connectors.
For the PostgreSQL if not already created please refer to
[Setup Operational Database](../../infra/README.md#4-how-to-setup-operational-database) documentation for
instructions on how to create the users, databases and tables required for this lab.

To maintain isolation of each domain in MinIO the approach to configure the buckets is to create an user
for each domain/bucket only with the required access. To do so, you
should connect to MinIO using their cli interface from inside the cluster:

```shell
kubectl run miniocli --rm -i --tty --image minio/mc --namespace storage --command /bin/sh
```

Inside the container you should configure your MinioCLI to connect to the cluster by doing:

```shell
mc alias set local minio.storage.svc.cluster.local:80 <MINIO_ADMIN_USER> <MINIO_ADMIN_PASSWORD>
```

You can now create the users for each domain by running the following commands:

```shell
mc admin user add local s3sink_business <PASSWORD>
mc admin user add local s3sink_checkin <PASSWORD>
mc admin user add local s3sink_evaluations <PASSWORD>
mc admin user add local s3sink_user <PASSWORD>
```

With the users create, now you can create and attach the required policies for each user. This can be done
by running the command below for each domain/bucket, replacing the <BUCKET_NAME> and the <DOMAIN>.

> [!NOTE]
> You can copy the contents for each policy on [scripts folder](../../scripts/minio/).

```shell
cat > minio-<DOMAIN>-user-policy.json <<-END
{
   "Version":"2012-10-17",
   "Statement":[
     {
         "Effect":"Allow",
         "Action":[
           "s3:ListAllMyBuckets"
         ],
         "Resource":"arn:aws:s3:::*"
     },
     {
         "Effect":"Allow",
         "Action":[
           "s3:ListBucket",
           "s3:GetBucketLocation"
         ],
         "Resource":"arn:aws:s3:::<BUCKET_NAME>"
     },
     {
         "Effect":"Allow",
         "Action":[
           "s3:PutObject",
           "s3:GetObject",
           "s3:AbortMultipartUpload",
           "s3:PutObjectTagging"
         ],
         "Resource":"arn:aws:s3:::<BUCKET_NAME>/*"
     }
   ]
}
END
```

You can now create:

```shell
mc admin policy create local business-s3-sink minio-business-user-policy.json
mc admin policy create local checkin-s3-sink minio-checkin-user-policy.json
mc admin policy create local evaluations-s3-sink minio-evaluations-user-policy.json
mc admin policy create local user-s3-sink minio-user-user-policy.json
```

And attach the policies for each user:

```shell
mc admin policy attach local business-s3-sink --user s3sink_business
mc admin policy attach local checkin-s3-sink --user s3sink_checkin
mc admin policy attach local evaluations-s3-sink --user s3sink_evaluations
mc admin policy attach local user-s3-sink --user s3sink_user
```

With all this setup, you can now add all these secrets into the cluster again for each domain (replacing
the values between <>):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kafka-connect-<DOMAIN>-postgresql-user
  namespace: processing
type: Opaque
stringData:
  username: <DOMAIN_POSTGRESQL_USER>
  password: <DOMAIN_POSTGRESQL_PASSWORD>
---
apiVersion: v1
kind: Secret
metadata:
  name: kafka-connect-<DOMAIN>-minio-user
  namespace: processing
type: Opaque
stringData:
  username: <DOMAIN_MINIO_USER>
  password: <DOMAIN_MINIO_PASSWORD>
---
```

Before advancing to deployment it is important to get the internal IP address of a container registry that will
be used to create the image with the connector plugins. This is required because the Kafka Connect deployment
creates a custom image with the code required for each Connector that we are going to use and uplods it to a
container registry. To get this IP address you should consult the documentation of your cluster solution.

Assuming a CR deployed into a `container-registry` namespace and with a service name `registry`. In fact this
is microk8s default configuration for built-in container registry addon. The command below gets the required
IP and port for the container registry.

```shell
kubectl -n container-registry get svc registry -o jsonpath='{.spec.clusterIP}' # Get IP
kubectl -n container-registry get svc registry -o jsonpath='{.spec.ports}' # Get Ports
```

Replace the values above on `spec.build.output.image` of the `kafka-connect.yaml` file to create a valid tag
to push to the container registry. You can now deploy both the Kafka Connect cluster and its connectors.

```shell
kubectl apply -f infra/processing/kafka/kafka-connect-cluster.yaml
kubectl apply -f infra/processing/kafka/kafka-connect-connectors.yaml
```

### Hive Metastore

Hive metastore is deployed using a custom Kubernetes Manifest based on the
[Apache Hive Docker Image](https://hub.docker.com/r/apache/hive), this is required for Trino to be able to
query data on a S3-Like storage (in our case MinIO).

First of all, to persist information between deployments Hive Metastore requires a table in a SQL-like
database. The code below setups an user and the database required for the application. Note that the password
should use PostgreSQL MD5 hash format.

```shell
pyenv exec poetry run python scripts/postgresql-run-script.py infra/processing/hive-metastore/sql/setup-db.sql -s password=$(echo -n "md5"; echo -n "<PASSWORD>hivemetastore" | md5sum | sed 's/ .*$//')
```

With the user and database created, submit the required secrets as defined below replacing the values
`<USERNAME>`, `<PASSWORD>` and `<DATABASE>` with the credentials created before.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hive-db-secret
  namespace: processing
type: Opaque
stringData:
  hive-site.xml: |
    <?xml version="1.0"?>
    <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    <configuration>
      <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:postgresql://postgresql.storage.svc.cluster.local:5432/<DATABASE></value>
      </property>
      <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>org.postgresql.Driver</value>
      </property>
      <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>hivemetastore</value>
      </property>
      <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value><PASSWORD></value>
      </property>
    </configuration>
```

Now you can deploy the Metastore by running:

> ![WARNING]
> For the first deployment you need to setup the env variable `IS_RESUME` to False. This ensures that the
> Metastore will create all the required tables and files on the volume and on PostgreSQL. Change this
> value if it is the case, otherwise the deployment will not work correctly.

```shell
kubectl apply -f infra/processing/hive-metastore/metastore.yaml
```

> ![IMPORTANT]
> Don't forget to change back to `true` the value of `IS_RESUME`.

## FAQ

### 1. How can I create a ad-hoc snapshot of a table?

[Ad-hoc snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-ad-hoc-snapshots)
is a way to create snapshots after the initial one made by the PostgreSQL connector. This can be useful for
rebuilding things, for data corruption and many other uses. These snapshots can be create by interacting
with a signal table used by debezium for the user to send commands to the connectors. You can create a full
snapshot of a database by creating a signal into the database referred into each
connector `signal.data.collection` configuration (replacing the values between <>):

```sql
INSERT INTO debezium_signal VALUES (<ID>, 'execute-snapshot', '{"data-collections": [<TABLE_LIST>]}')
```

For example, if you have a database called `test` with two tables `table1` and `table2` and a signal table
named `debezium_signal` you can create a full snapshot by running the following command (in the database).

```sql
INSERT INTO debezium_signal VALUES (1, 'execute-snapshot', '{"data-collections": ["public.table1", "public.table2"]}')
```

Note that for the code above to work **it is required a PRIMARY KEY in the tables**. This is because Debezium
uses the primary key to sort and understand what is required to send. If this is not the case you can
use a surrogate-key parameter that will be used as the primary key.

```sql
INSERT INTO debezium_signal VALUES (1, 'execute-snapshot', '{"data-collections": ["public.table1", "public.table2"], "surrogate-key": "example-key"}')
```

> ![NOTE]
> For more information about ad-hoc snapshots
> read
> [Sending signals to a Debezium connector](https://debezium.io/documentation/reference/stable/configuration/signalling.html)
> and
> [PostgreSQL connector: Snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots)

## Further Reading

* [Kafka Docs](https://kafka.apache.org/documentation/#gettingStarted)
* [Debezium Docs](https://debezium.io/documentation/)
* [dbt Docs](https://docs.getdbt.com/)
* [Strimzi Operator Docs](https://strimzi.io/documentation/)
* [Strimzi: Deploy Debezium on Kubernetes](https://debezium.io/documentation/reference/stable/operations/kubernetes.html)
* [Strimzi Blog: Accessing Kafka: Part 2 - Node Ports](https://strimzi.io/blog/2019/04/23/accessing-kafka-part-2/)
* [Strimzi: Debezium Connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
* [Sending signals to a Debezium connector](https://debezium.io/documentation/reference/stable/configuration/signalling.html)
* [PostgreSQL connector: Snapshots](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-snapshots)
* [Hive Architecture](https://cwiki.apache.org/confluence/display/hive/design)
