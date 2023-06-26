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
