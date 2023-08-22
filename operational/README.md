# Operational

The purpose of [Yelp Dataset](https://www.yelp.com/dataset) is to be used for research purposes, because of
that some information are already aggregated (e.g. number of stars) or transformed in some way. To be able to
simulate all the steps from an operational data to an analytical data product, the objective of this
folder is to prepare this data in order to be as close as possible from what is believed to exist
in a real world scenario (giving the available data).

Some important takeways/assumptions:

* We are assuming that the analytical data will be available in a SQL database;
* Only one instance of PostgreSQL is used for all domains which is probably different in a real world
scenario where each domain manages it's own microservice (and related database), to mantain a certain degree
of isolation each domain will have its own database;
* Data will be preserved as close as possible from the available in the dataset, this is, with the minimum
number of transformations. The data products will handle the needed transformations;

For more information about how to run code or a deep understanding on the steps taken to prepare the data
see each notebook.

> **Note** </br>
> For a deeper understanding about this code it is important that you fully understand the
> [Logical Architecture](../docs/logical-architecture.md). You can also read more about the
> [Platform Architecture](../infra/README.md).
