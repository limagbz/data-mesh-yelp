# Data Product

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

This project aims to emulate a complete data product. This means, data collection,
monitoring, modeling, operations and anything that can be added for the construction of a data product.

Note that this is not a production-ready project, instead it aims to help me study, understand some concepts
of data engineering (mainly data meshs, but not exclusively), test some beliefs and see on practice how things
work. This project will evolve as my knowledge evolves so drastic changes can occur during the development.

## Architecture

![architecture](architecture.drawio.png)

## Setup your local environment

> **Note** </br>
> In order to deploy the resources a kubernetes cluster is required. There are a lot of ways to deploy a
> kubernetes cluster locally however this is out of the scope of this documentation.
> [MicroK8S](https://microk8s.io/) was the chosen way to deploy a cluster for this project, however there are
> many solutions out there, you can see some examples on
> [Kubernetes: Install Tools](https://kubernetes.io/docs/tasks/tools/).

For those who uses VSCode, this project comes with a full-featured dev container containing all the tools,
some extensions and configurations required to work with the project. If you don't know this feature, please
read [Visual Studio Code: Developing Inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).

For people that do not use, please refer to the [Dockerfile](.devcontainer/Dockerfile) for a list of installed
tools and versions.

## Contributing

> **Warning** </br>
> Please, read the [CONTRIBUTING Guide](CONTRIBUTING.md) for more details about how to contribute with this
> project.

You can use the **discussion** tabs to propose new features/improvements, ask questions and engage with the
community. This is the main source of issues to improve the codebase. To file bug reports you can directly
use the **issues** tab (with the bug template).

Finally, you can also implement improvements by creating **pull requests**, however we suggest reading the
issues and discussions first. Don't forget to read our [CONTRIBUTING Guide](CONTRIBUTING.md).

## Further Readings

* [Data Mesh Architecture](https://www.datamesh-architecture.com/)
* [Data Mesh Architecture (Tech Stack): dbt and Snowflake](https://www.datamesh-architecture.com/tech-stacks/dbt-snowflake)
* [Data Mesh Architecture (Tech Stack): MinIO and Trino](https://www.datamesh-architecture.com/tech-stacks/minio-trino)
* [MicroK8S](https://microk8s.io/)
