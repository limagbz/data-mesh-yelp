# Infrastructure

This directory contains all the infrastructure deployed into kubernetes and required for this project.
Note that each subfolder represents a namespace inside the cluster.

<p align="center">
<img src="../docs/_static/diagrams/platform-architecture.drawio.png" />
</p>

## Features

* Prometheus monitoring system to collect metrics for all kubernetes pods and nodes;
* Grafana for metrics visualization and graphs;
* MinIO Object storage to store data from lots of sources including data from pipelines;
* Airflow and required resources to manage the pipelines;
