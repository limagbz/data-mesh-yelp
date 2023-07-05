# Processing

This namespace contains all the required resources for processing data (e.g. Airflow and DBT) and related
resources. For full information about all the resources on the cluster see [README](../README.md).

## Step-by-Step Deployment

### 0. Deploy Namespace

```shell
kubectl apply -f infra/processing/namespace.yaml
```

### 1. Deploy Airflow (v2.6.2)

This approach of deploying airflow uses a Persistent Volume (without git sync) to store the DAGs. This
enables a faster development and its ok for a non-production environments. To deploy the **Local** Persistent
Volume and its respective claim.

> **Warning** </br>
> Make sure that the local path created on the node. Change the value on `spec.local.path` on
> `airflow/dags-pvc.yaml` if necessary for your setup.

```shell
kubectl apply -f infra/processing/airflow/dags-pvc.yaml
```

Also, to prevent secrets in the charts, some secrets need to be created for Airflow and related resources.
This can be done by creating secrets using the templates below, replacing the values between <>:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secrets
  namespace: processing
stringData:
  postgres-password: <POSTGRES_ADMIN_PASSWORD>
  user-password: <POSTGRES_USER_PASSWORD>
  replication-password: <POSTGRES_REPLICATION_PASSWORD>
---
apiVersion: v1
kind: Secret
metadata:
  name: airflow-redis-secret
  namespace: processing
stringData:
  redis-password: <REDIS_PASSWORD>
---
apiVersion: v1
kind: Secret
metadata:
  name: airflow-metadata-secret
  namespace: processing
stringData:
  connection: postgresql://airflow-user:<POSTGRES_USER_PASSWORD>@airflow-postgresql.processing:5432/postgres
---
apiVersion: v1
kind: Secret
metadata:
  name: airflow-webserver-secret
  namespace: processing
stringData:
  webserver-secret-key: <AIRFLOW_WEBSERVER_SECRET_KEY>  # Continue reading for how to generate this value
```

For `<AIRFLOW_WEBSERVER_SECRET_KEY>` you can generate a value by running the command below into your terminal

```shell
python3 -c 'import secrets; print(secrets.token_hex(16))'
```

Finally you can deploy airflow using helm by running:

```shell
helm install -f infra/processing/airflow/values.yaml airflow infra/processing/airflow/helm -n processing
```

## FAQ

### How to create an Admin user for Airflow?

You can run the command below to create an user with Admin role on Airflow, replacing the values between <>:

```shell
kubectl exec -n processing --stdin --tty $(kubectl get pods --all-namespaces -o=name | grep "airflow-webserver" | sed "s/^.\{4\}//") -- airflow users create \
  --username <USERNAME> \
  --firstname <FIRSTNAME> \
  --lastname <LASTNAME> \
  --role Admin \
  --email <EMAIL> \
  --password <PASSWORD>
```

### How to deploy dags on Airflow?

You can run the command below to copy the dags from the `dags` folder into Airflow:

```shell
kubectl cp dags/ $(kubectl get pods --all-namespaces -o=name | grep "airflow-scheduler" | sed "s/^.\{4\}//"):/opt/airflow/dags -n processing
```
