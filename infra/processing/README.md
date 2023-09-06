# Processing

1. [Overview](#overview)
1. [Step-by-Step Deployment](#step-by-step-deployment)
1. [FAQ](#faq)
1. [Further Reading](#further-reading)

## Overview

Here is all the processing infrastructure for the data mesh to Work. From
[Kafka](https://kafka.apache.org/documentation/#gettingStarted) and
[Debezium](https://debezium.io/documentation/) used to send
the operational data right into the storage for analytics, also [dbt](https://docs.getdbt.com/) to process
the data into products.

## Step-by-Step Deployment

### 0. Deploy Namespace

All the resources above will be deployed in a single namespace. This can be done by running:

```shell
kubectl apply -f infra/processing/namespace.yaml
```

### 1. Deploy Kafka (and Kafka Connect)

All the Kafka resources will be deployed using the [Strimzi Operator](https://strimzi.io/). The features
of this chart includes many Kafka resources such as Kafka Connect, Exporter, MirrorMaker, Bridge and many
other components. To deploy the operator:

```shell
helm install -f infra/processing/kafka/values.yaml kafka-operator infra/processing/kafka/helm -n processing
```

With the operator deployed it is necessary to deploy the cluster and related resources such as Zookeeper
(for brokers and consumers coordination), and Exporter (for metrics)

```shell
kubectl apply -f infra/processing/kafka/kafka-cluster.yaml
```

Now that the cluster is created, we need to create the Kafka Connect framework and its connectors: Debezium
to get changes from Postgres and Confluent to send data to S3/MinIO. First create the required
secrets used by the connectors.

> **Warning** </br>
> The postgres user requires REPLICATION permission for the connector to work properly. See
> [Postgres Connector: Setting Permissions](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-permissions)
> for more information.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kafka-connect-postgres-user
  namespace: processing
type: Opaque
stringData:
  username: <POSTGRES_USER>
  password: <POSTGRES_PASSWORD>
---
apiVersion: v1
kind: Secret
metadata:
  name: kafka-connect-s3-user
  namespace: processing
type: Opaque
stringData:
  id: <SECRET_ACCESS_KEY_ID>
  secret-key:  <SECRET_KEY>
```

Before advancing to deployment it is important to get the internal IP address of a container registry that will
be used to create the image with the connector plugins. Below an example command that can be used assuming
a CR deployed into a `container-registry` namespace and with a service name `registry` (in fact this is
microk8s default configuration for built-in container registry addon).

```shell
kubectl -n container-registry get svc registry -o jsonpath='{.spec.clusterIP}' # Get IP
kubectl -n container-registry get svc registry -o jsonpath='{.spec.ports}' # Get Ports
```

Replace the values above on `spec.build.output.image` of the `kafka-connect.yaml` file to create a valid tag
to push to the container registry. These connectors are also feature with
[debezium signaling](https://debezium.io/documentation/reference/stable/configuration/signalling.html) to
interact with the connectors. To use this it is required to setup a table for each database that have a
connector attached to it. A helper script was created on this folder. For it to work it is required to
Create a file .env with the following information (they will be loaded automatically when running the script).

```shell
POSTGRESQL_USER=<POSTGRES_USER>
POSTGRESQL_PASSWORD=<POSTGRES_PASSWORD>
POSTGRESQL_HOST=<POSTGRES_HOST>
POSTGRESQL_PORT=<POSTGRES_PORT>
```

You can now run the script

```shell
pyenv exec poetry run python infra/processing/kafka/scripts/create-signals-database.py
```

> **Note** </br>
> For the purpose of this lab, this script is executed from the local machine. Another better approach
> is to create a kubernetes job that do this setup and is executed with the deployment of the resources.

Now it is safe to deploy Kafka Connect and its connectors.

> **Warning** </br>
> The databases and buckets referred on the connectors should exist before deploying the connectors. Make
> sure this is true before running the command below. On this lab this means running the
> [Operational Data Setup](../../operational/setup-operational-data.ipynb) for the databases. The buckets
> are created together with MinIO deployment.

```shell
kubectl apply -f infra/processing/kafka/kafka-connect.yaml
```

## FAQ

### 1. Where to see errors in Connector deployments?

When deploying the connector a good place to see the errors are in the Kafka Connector CRD. By inspecting
the objects you can see any error that may ocurred.

### 2. How can I create a ad-hoc snapshot of a table?

You can create a full snapshot of a database by creating a signal into the database referred into each
connector `signal.data.collection` configuration (replacing the values between <>):

```sql
INSERT INTO debezium_signal VALUES (<ID>, 'execute-snapshot', '{"data-collections": [<TABLE_LIST>]}')
```

For example, if you have a database called `test` with two tables `table1` and `table2` and a signal table
named `debezium_signal` you can create a full snapshot by running the following command (in the database).

```sql
INSERT INTO debezium_signal VALUES (1, 'execute-snapshot', '{"data-collections": ["public.table1", "public.table2"]}')
```

> **Warning** </br>
> For this to work the tables should contain a PRIMARY KEY. For more information about ad-hoc snapshots
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
