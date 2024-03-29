# Monitoring

1. [Overview](#overview)
1. [Deployment Guide](#deployment-guide)
1. [FAQ](#faq)
1. [Further Reading](#further-reading)

## Overview

This namespace contains all the required resources for monitoring the cluster and its resources. This
includes: [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) an agent deployed in
every machine (Daemon Set) that needs to be monitored and is used to discover and send
logs from these machines to a Loki Instance. [Grafana Loki](https://grafana.com/docs/loki/latest/) is them
used to manage and centralize all the logs from the cluster. We also have
[Prometheus](https://prometheus.io/docs/introduction/overview/) that centralize all metrics exported
by pods, nodes and other resources for the cluster. Finally is
[Grafana](https://grafana.com/docs/grafana/latest/) used in  this project to visualize all this collected
information (i.e. logs and metrics) in useful dashboards and manage alerts.

## Deployment Guide

> [!WARNING]
> Before deploying any resource on this folder, please create the namespace by running:
> `kubectl apply -f infra/monitoring/namespace.yaml`

### Prometheus

Prometheus is deployed using [Prometheus Helm Chart](https://github.com/prometheus-community/helm-charts/tree/prometheus-22.6.4/charts/prometheus)
from [Prometheus Community](https://github.com/prometheus-community). This chart have many features including
Prometheus Push Gateway, Alert Manager and others (see the [`prometheus/helm/values.yaml`](prometheus/helm/values.yaml))
for detailed information about each feature and [`prometheus/values.yaml`](prometheus/values.yaml) for
details on what this project uses.

```shell
helm install -f infra/monitoring/prometheus/values.yaml prometheus infra/monitoring/prometheus/helm -n monitoring
```

### Grafana Loki

Loki is also deployed using an official Helm chart. The
[Loki helm chart by Grafana](https://artifacthub.io/packages/helm/grafana/loki) also contains many features,
see [`loki/values.yaml`](loki/values.yaml) for details on what this project uses. To deploy this chart,
first you need to create the credentials for the gateway that manages the connection to Loki. This can be
done by running the command below, replacing the value `<LOKI_GATEWAY_USER>` with the wanted username.

> [!NOTE]
> See [NGINX: Restricting Access with HTTP Basic Authentication](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/#creating-a-password-file)
> for more information

```shell
htpasswd -c .htpasswd <LOKI_GATEWAY_USER>
```

The command above will ask for a password. A file `.htpasswd` will be generated on the folder that you
executed the command. Copy the contents of this file and paste it on a secret as shown below. Don't forget
to apply the secrets with `kubectl apply`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: loki-gateway-auth
  namespace: monitoring
stringData:
  .htpasswd: |
    <CONTENT_FROM_HTPASSWRD_FILE>
```

You also need to create another secret for Loki to connect to a Minio tenant as described below. Don't forget
to apply the secrets with `kubectl apply`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: loki-s3-secret
  namespace: monitoring
stringData:
  S3_LOKI_ACCESS_KEY_ID: <MINIO_ACCESS_KEY_ID>
  S3_LOKI_SECRET_ACCESS_KEY: <MINIO_SECRET_ACCESS_KEY>
```

After that, just deploy Loki by running the helm command below:

```shell
helm install -f infra/monitoring/loki/values.yaml loki infra/monitoring/loki/helm -n monitoring
```

### Promtail

Promtail is deployed using the official
[Promtail Helm Chart by Grafana](https://artifacthub.io/packages/helm/grafana/promtail). To be able to
connect with Loki using the gateway first create a secret with the original password (not the htpasswd one).
Don't forget to apply the secrets with `kubectl apply`:

> [!WARNING]
> The secret below will also be used for Grafana deployment

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: loki-gateway-password
  namespace: monitoring
stringData:
  LOKI_GATEWAY_PASSWORD: <LOKI_GATEWAY_PASSWORD>
```

Now that everything is setup, just run the command below to deploy promtail

```shell
helm install -f infra/monitoring/promtail/values.yaml promtail infra/monitoring/promtail/helm -n monitoring
```

### Grafana

Grafana is deployed by using the official Grafana Helm Chart. You can find more information about the chart
on [Deploy Grafana on Kubernetes](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/).
To deploy the chart contained in this repo, first you need to create the admin user and password by
configuring a secret as described below, replacing the values  `<GRAFANA_USER>` and `<GRAFANA_PASSWORD>` with
your own values. Don't forget to apply the secrets with `kubectl apply`.

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

### 1. Metrics and Logs are scraped automatically for each new application?

Yes and No. To scrape metrics for Prometheus it is required that you add at least the
`prometheus.io/scrape: "true"` annotation in the pods/service-endpoints that have prometheus-compatible
metrics (see other questions in this FAQ for more details). For logs, promtail is deployed as a Daemon Set
that collects every machine that needs to be monitored. So it doesn't require an specific configuration.

### 2. How to scrape metrics from pods using Prometheus?

Assuming the pod/application expose metrics compatible with prometheus. You only need to add the following
annotation in the pod that they will be automatically scraped:

```yaml
prometheus.io/scrape: "true"
prometheus.io/scheme: # If the metrics endpoint is secured then you will need to set this to `https` & most likely set the `tls_config` of the scrape config.
prometheus.io/path:   # If the metrics path is not `/metrics` override this.
prometheus.io/port:   # Scrape the pod on the indicated port instead of the default.
```

### 3. How to scrape metrics from service endpoints using Prometheus?

The approach is similar to scrape metrics from pods. Add the following annotations

```yaml
prometheus.io/scrape: "true"
prometheus.io/scheme: # If the metrics endpoint is secured then you will need to set this to `https` & most likely set the `tls_config` of the scrape config.
prometheus.io/path:   # If the metrics path is not `/metrics` override this.
prometheus.io/port:   # Scrape the pod on the indicated port instead of the default.
prometheus.io/param_<parameter>: # If the metrics endpoint uses parameters then you can set any parameter
```

### 4. How to deploy Dashboards via JSON file?

For this you need to add the json files representing the dashboards into the folder `grafana/helm/dashboards`.
Don't forget to also edit the `values.yaml` file to add their paths.

## Further Reading

* [Promtail Installation](https://grafana.com/docs/loki/latest/clients/promtail/installation/).
* [Deploy Grafana on Kubernetes](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/).
* [Install Grafana Loki with Helm](https://grafana.com/docs/loki/latest/installation/helm/#install-grafana-loki-with-helm).
* [How to collect and query Kubernetes logs with Grafana Loki, Grafana, and Grafana Agent](https://grafana.com/blog/2023/04/12/how-to-collect-and-query-kubernetes-logs-with-grafana-loki-grafana-and-grafana-agent/)
