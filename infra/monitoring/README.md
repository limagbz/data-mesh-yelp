# Monitoring

This namespace contains all the required resources for monitoring the cluster and its resources. For full
information about all the resources on the cluster see [README](../README.md)

## Step-by-Step Deployment

### 0. Deploy namespace

```shell
kubectl apply -f infra/monitoring/namespace.yaml
```

### 1. Deploy Prometheus (v0.65.2)

Prometheus is deployed using the prometheus-operator helm chart that is mantained by the community. You can
find more information about the chart on their
[Prometheus Community: Prometheus Chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus).
To deploy just do the following (from the root folder of the project):

```shell
helm install -f infra/monitoring/prometheus/values.yaml prometheus infra/monitoring/prometheus/helm -n monitoring
```

### 2. Deploy Grafana  (v6.57.2)

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

## FAQ

### 1. How to scrape metrics from pods using Prometheus?

Assuming the pod/application expose metrics compatible with prometheus. You only need to add the following
annotation in the pod that they will be automatically scraped:

```yaml
prometheus.io/scrape: # Only scrape pods that have a value of `true`, except if `prometheus.io/scrape-slow` is set to `true` as well.
prometheus.io/scheme: # If the metrics endpoint is secured then you will need to set this to `https` & most likely set the `tls_config` of the scrape config.
prometheus.io/path:   # If the metrics path is not `/metrics` override this.
prometheus.io/port:   # Scrape the pod on the indicated port instead of the default of `9102`.
```
