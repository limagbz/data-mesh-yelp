# Infrastructure

This folder contains all the infrastructure required for this project to work. All this infrastructure is
deployed in a kubernetes cluster. For a simplified view of the architecture see the project's
[README](../README.md).

## Features

* Prometheus monitoring system to collect metrics for all kubernetes pods and nodes;
* Grafana for metrics visualization and graphs;
* MinIO Object storage to store data from lots of sources including data from pipelines;
