# Storage

1. [Overview](#overview)
1. [Deployment Guide](#deployment-guide)
1. [FAQ](#faq)
1. [Further Reading](#further-reading)

## Overview

This namespace contains all the resources required to store data for the operational and analytics parts of
the project. This includes: A [PostgreSQL](https://www.postgresql.org/) database to store operational data
and to be support of other systems that require an SQL like database and a [MinIO](https://min.io/) tenant
to store objects.

## Deployment Guide

> [!WARNING]
> Before deploying any resource on this folder, please create the namespace by running:
> `kubectl apply -f infra/storage/namespace.yaml`

### PostgreSQL

PostgreSQL is deployed using the
[Bitnami Helm Chart](https://artifacthub.io/packages/helm/bitnami/postgresql). To deploy the database
first you need to setup the required secrets. This can be done by creating a secret with the template below
replacing the value of `<ADMIN_PASSWORD>` with the password for the `postgres` admin user. Don't forget to
apply the secrets with `kubectl apply`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secrets
  namespace: storage
stringData:
  admin-password: <ADMIN_PASSWORD>
```

Now you can just deploy the database running the command below:

```shell
helm install -f infra/storage/postgresql/values.yaml postgresql infra/storage/postgresql/helm -n storage
```

### MinIO: Operator and Tenant

To deploy Minio we first need to deploy its operator. You can see more about the ofifcial operator and how to
deploy on [Deploy Operator With Helm](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html).
To deploy the operator:

```shell
helm install -f infra/storage/minio/values-operator.yaml minio-operator infra/storage/minio/helm/operator -n storage
```

Currently there is no straightforward way to setup Node Ports for accessing the operator UI. In this case
we are going to patch this service in order to access:

```shell
kubectl patch svc console --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30210},{"op":"replace","path":"/spec/ports/1/nodePort","value":30211}]' -n storage
```

With the operator up we can deploy the tenant using the other Helm Chart. But first we need to configure
the admin user (and its password) for MinIO by applying the secret as defined below replacing the values
between <>. See
[Deploy a Tenant](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html#deploy-a-tenant)
for more information about how to deploy a tenant. Don't forget to run `kubectl apply`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-admin-user
  namespace: storage
stringData:
  config.env: |-
    export MINIO_ROOT_USER="<MINIO_USER>"
    export MINIO_ROOT_PASSWORD="<MINIO_PASSWORD>"
```

Then, you only need to deploy the tenant by running:

```shell
helm install -f infra/storage/minio/values-tenant.yaml minio-tenant infra/storage/minio/helm/tenant -n storage
```

> [!NOTE]
> Trying to patch the tenant services to use NodePort raises a problem on the operator as it detects changes
> that were done externally. The recommended way to connect with the tenant console is through Ingress (or
> port forward). However from the Operator Console we still can access the tenant console.

## FAQ

### 1. How to connect with PostgreSQL?

Using your preferred tool (e.g. [pgAdmin](https://www.pgadmin.org/), [DBeaver](https://dbeaver.io/),
postgres-cli) you can use the created credentials for the admin on any database. You can also use the user
and the database defined in the `auth` section of the `values.yaml` file.

### 2. How can I get access to MinIO (Operator) Console?

To authenticate with MinIO Operator console you need to get a JWT token to authenticate. This can be done by
running the command below. Note that the Operator Console is different than the MinIO console. On the
operator's you have access to create different tenants and can also access each Tenant.

```shell
echo $(kubectl -n storage  get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode)
```

## Further Reading

* [Bitnami: Differences between the PostgreSQL-HA and PostgreSQL Helm charts](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/get-started/compare-solutions/)
* [PostgreSQL packaged by Bitnami for Kubernetes](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/)
* [MinIO Object Storage for Kubernetes](https://min.io/docs/minio/kubernetes/upstream/index.html)
