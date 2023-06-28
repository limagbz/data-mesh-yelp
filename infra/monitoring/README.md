# Monitoring

This namespace contains all the required resources for monitoring the cluster and its resources.

## Step-by-Step Deployment

### 0. Deploy namespace

```shell
kubectl apply -f infra/monitoring/namespace.yaml
```

### 1. Deploy Prometheus (v0.65.2)

Prometheus is deployed using the prometheus-operator helm chart that is mantained by the community. You can
find more information about the chart on their
[Getting Started Guide](https://prometheus-operator.dev/docs/user-guides/getting-started/). To deploy just
do the following (from the root folder of the project):

```shell
helm install -f infra/monitoring/prometheus/values.yaml prometheus infra/monitoring/prometheus/helm -n monitoring
```

## 2. Deploy Grafana  (v6.57.2)

Grafana is deployed by using the official Grafana Helm Chart. You can find more information about the chart
on [Deploy Grafana on Kubernetes](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/).

To deploy the chart contained in this repo, first you need to create the admin user and password by
configuring a secret as described below, replacing the values  `<GRAFANA_USER>` and `<GRAFANA_PASSWORD>`

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: grafana-admin-user-password
  namespace: monitoring
stringData:
  admin-user: <GRAFANA_USER>
  admin-password: <GRAFANA_PASSWORD>
```

After that, just deploy Grafana by running the helm command below:

```shell
helm install -f infra/monitoring/grafana/values.yaml grafana infra/monitoring/grafana/helm -n monitoring
```
