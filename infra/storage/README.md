# Storage

This namespace contains all the required storage resources for the project to work, this includes mainly
databases, object storages (e.g. minio) and related resources. For full information about all the resources
on the cluster see [README](../README.md).

## Step-by-Step Deployment

```shell
kubectl apply -f infra/storage/namespace.yaml
```

### 1. Deploy MinIO Operator (v5.0.5)

To deploy Minio we first need to deploy its operator. You can see more about the official operator and how to
deploy on
[Deploy Operator With Helm](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html).
To deploy the operator just do the following (from the root folder of the project):

```shell
helm install -f infra/storage/minio/values-operator.yaml minio-operator infra/storage/minio/helm/operator -n storage
```

To be able to access the interface for the operator without ingress (since this project is not supposed to
run on a production environment) unfortunately there is no straightforward way to do this directly from the
helm chart values. So, it is necessary to patch the service in order to modify the service from a ClusterIP
to a NodePort. This can be done by:

```shell
kubectl patch svc console --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30200},{"op":"replace","path":"/spec/ports/1/nodePort","value":30201}]' -n storage
```

> **Note** </br>
> Note that the command above change add the HTTP port of the operator to 30200 and HTTPS to 30201. If you
> want, just modify the values of the ports.

### 2. Deploy MinIO Tenant (v5.0.5)

Now we can use the operator do deploy the tenant (with another helm chart). See
[Deploy a Tenant](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html#deploy-a-tenant) in
[Deploy Operator With Helm](https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html)
documentation for more information about how to deploy a tenant.

First of all it is required to deploy the root user and password. For this you need to apply a secret in the
following below, replacing the values `<MINIO_USER>` and `<MINIO_PASSWORD>`:

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
> Don't forget to run `kubectl apply`

Then, you only need to deploy the tenant by running:

```shell
helm install -f infra/storage/minio/values-tenant.yaml minio-tenant infra/storage/minio/helm/tenant -n storage
```

As done in the operator part, for non-production purposes we are going to use a node port to expose both
the tenant console. This can be done by running the following commands:

```shell
# Console
kubectl patch svc minio-data-tenant-console --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"},{"op":"replace","path":"/spec/ports/0/nodePort","value":30202}]' -n storage
```

> **Note** </br>
> You can also access the tenant console through the operator's console

## FAQ

### How to get Access Token for Minio?

```shell
SA_TOKEN=$(kubectl -n storage get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode) && echo $SA_TOKEN
```
