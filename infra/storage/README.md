# Storage

1. [Overview](#overview)
1. [Step-by-Step Deployment](#step-by-step-deployment)
1. [FAQ](#faq)
1. [Further Reading](#further-reading)

## Overview

This namespace contains all the required storage resources for the project to work, this includes mainly
databases (e.g. PostgreSQL), object storages (e.g. minio) and related resources. For full information about
all the resources on the cluster see [README](../README.md).

## Step-by-Step Deployment

### 1. Create the namespace

All the resources above will be deployed in a single namespace. This can be done by running:

```shell
kubectl apply -f infra/storage/namespace.yaml
```

### 2. Deploy PostgreSQL

PostgreSQL is deployed using the
[Bitnami Helm Chart](https://artifacthub.io/packages/helm/bitnami/postgresql). Before deploying the database
you first need to setup the required secrets. This can be done by creating a secret with the template below.
Replacing the value of `<ADMIN_PASSWORD>` with the password for the `postgres` admin user and the
`<USER_PASSWORD>` with the password for the user specified in the `auth.username` on the `values.yaml` file.
Don't forget to apply the secrets with `kubectl apply`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secrets
  namespace: storage
stringData:
  admin-password: <ADMIN_PASSWORD>
  user-password: <USER_PASSWORD>
```

Now you can just deploy the database running the command below:

```shell
helm install -f infra/storage/postgresql/values.yaml postgresql infra/storage/postgresql/helm -n storage
```

### 3. Deploy MinIO Operator and Console

To deploy Minio we first need to deploy its operator. You can see more about the official operator and how to
deploy on [Deploy Operator With Helm](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html).
To deploy the operator just do the following (from the root folder of the project):

```shell
helm install -f infra/storage/minio/values-operator.yaml minio-operator infra/storage/minio/helm/operator -n storage
```
To be able to access the interface for the operator without ingress (since this project is not supposed to
run on a production environment) unfortunately there is no straightforward way to do this directly from the
helm chart values. So, it is necessary to patch the service in order to modify the service from a ClusterIP
to a NodePort. This can be done by:

```shell
kubectl patch svc console --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30210},{"op":"replace","path":"/spec/ports/1/nodePort","value":30211}]' -n storage
```

> **Note** </br>
> Note that the command above change add the HTTP port of the operator to 30200 and HTTPS to 30201. If you
> want, just modify the values of the ports.

### 4. Deploy MinIO Tenant (v5.0.5)

Now we can use the operator do deploy the tenant (with another helm chart). See
[Deploy a Tenant](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html#deploy-a-tenant) for more information about how to deploy a tenant.

First of all it is required to deploy the root user and password. For this you need to apply a secret in the
following below, replacing the values <MINIO_USER> and <MINIO_PASSWORD>:

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

> **Note** </br>
> Don't forget to run kubectl apply

Then, you only need to deploy the tenant by running:

```shell
helm install -f infra/storage/minio/values-tenant.yaml minio-tenant infra/storage/minio/helm/tenant -n storage
```

We also use the same approach used on the operator to enable access to the services via NodePort (by patching
the services).

```shell
# Service used for systems interact with MinIO
kubectl patch svc minio --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30212}]' -n storage

# MinIO Console
kubectl patch svc minio-data-tenant-console --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30213}]' -n storage
```

## FAQ

### 1. How to connect with PostgreSQL?

Using your preferred tool (e.g. [pgAdmin](https://www.pgadmin.org/), [DBeaver](https://dbeaver.io/),
postgres-cli) you can use the created credentials for the admin on any database. You can also use the user
and the database defined in the `auth` section of the `values.yaml` file.

### 2. How can I get access to MinIO (Operator) Console?

To authenticate with MinIO Operator console you need to get a JWT token to authenticate. This can be done by
running the command below. Note that the Operator Console is different than the MinIO console. On the
operator's you have access to create different tenants and can also access each Tenant. The MinIO Console
(the one used to manage the Tenant) can be accessed using the credentials used on the deployment

```shell
echo $(kubectl -n storage  get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode)
```

## Further Reading

* [Bitnami: Differences between the PostgreSQL-HA and PostgreSQL Helm charts](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/get-started/compare-solutions/)
* [PostgreSQL packaged by Bitnami for Kubernetes](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/)
* [MinIO Object Storage for Kubernetes](https://min.io/docs/minio/kubernetes/upstream/index.html)
