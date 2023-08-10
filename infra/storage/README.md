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

## FAQ

### 1. How to connect with PostgreSQL

Using your preferred tool (e.g. [pgAdmin](https://www.pgadmin.org/), [DBeaver](https://dbeaver.io/),
postgres-cli) you can use the created credentials for the admin on any database. You can also use the user
and the database defined in the `auth` section of the `values.yaml` file.

## Further Reading

* [Bitnami: Differences between the PostgreSQL-HA and PostgreSQL Helm charts](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/get-started/compare-solutions/)
* [PostgreSQL packaged by Bitnami for Kubernetes](https://docs.bitnami.com/kubernetes/infrastructure/postgresql/)
