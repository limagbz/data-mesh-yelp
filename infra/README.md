# Infrastructure

1. [Architecture](#architecture)
1. [Data Platform](#data-platform)
1. [Other Resources](#other-resources)
1. [FAQ](#faq)

## Architecture

<p align="center">
<img src="../docs/_static/architecture/platform-architecture.drawio.png" />
</p>

## Data Platform

Below is the description of all the resources deployed for the central self-serve data platform as defined
in the data mesh architecture. This is, that are managed by an data-platform team and not by the domains.

### Monitoring Stack (Grafana, Loki and Prometheus)

To achieve a better observability all the resources of the platform are monitored via
Prometheus + Loki + Grafana Stack. The role of **Prometheus** is to centralize all the metrics generated for each
tool (and also cluster resources) if the metrics are available. The same idea is implemented by
**Grafana Loki** but instead of metrics it collects logs, this is useful for a more complete overview of
the state of the platform. Finally, all these metrics and logs can be visualized on **Grafana** for people
to be able to take action. Is also on Grafana that alerts are managed based on the received information.

<p float="left" align="center">
  <img src="../docs/_static/screenshots/grafana-cluster-monitoring.png" width="36%" />
  <img src="../docs/_static/screenshots/grafana-log-monitoring.png" width="49%" />
</p>

### Object Storage (MinIO)

To store all the data used in the project a MinIO tenant is deployed. This data will be queried using Trino
and transformed using dbt.

<!-- TODO: Explain how data is organized, lifecycle policies and configurations when ready.  -->
<!-- TODO: Add a screenshot when some data is already added  -->

> **Note** </br>
> MinIO is also used by other applications such as Grafana Loki to store data.

## Other Resources

Below are the resources used in the lab that are not directly a part of the centralized data platform and
that are created to support this lab in some way.

### PostgreSQL (Operational Data)

PostgreSQL is used to simulate the operational database that stores the information coming from Yelp page
for each domain. See [operational](../operational/) folder for more information about how the data is
created into the database.

> **Note** </br>
> For simplicity (and resource management) only one instance of postgres will be deployed for all domains
> (with a separated database for each one to achieve isolation). On a real world example this architecture
> can change since each domain operates their own microservices.

<p float="left" align="center">
  <img src="../docs/_static/screenshots/postgres.png" width="60%" />
</p>

## FAQ

### 1. How to access the services?

This project was created using a local machine running a Kubernetes Cluster. For simplicity all the relevant
services are exposed via NodePort (see table below for ports).

| **Application/Service**        | **Port**  |
| ------------------------------ | --------- |
| Prometheus                     | 30100     |
| Grafana                        | 30110     |
| Loki Gateway                   | 30120     |
| PostgreSQL (Primary)           | 30200     |
| MinIO Operator Console (http)  | 30210     |
| MinIO Operator Console (https) | 30211     |
| MinIO Tenant                   | 30212     |
| MinIO Tenant Console           | 30213     |

### 2. Can I use this infrastructure for a production environment?

Because this is not intended for a production environment, some things were simplified such as security
measures (e.g. SSL, Network Policies and other cluster security measures), access control (e.g. Ingress).
For this kind of use it is important that some best practices and recommended measures are followed.
