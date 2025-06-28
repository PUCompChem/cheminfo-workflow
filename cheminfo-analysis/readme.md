# Cheminfo Workflow

A Ploomber-based workflow for analyzing chemical and structural data from `.xlsx`/`.csv` files.

## Overview

This workflow supports clustering of chemical property data using a configurable set of parameters. It allows users to select specific columns and apply a clustering method (e.g., Ward, single linkage) with various distance metrics. The goal is to enable insightful groupings of chemical compounds or polymers based on selected descriptors.

---

## Parameters

All parameters are defined in `env.yaml`, but can also be overridden from the terminal.

| Parameter        | Type          | Description                                                                                     | Default       |
|------------------|---------------|-------------------------------------------------------------------------------------------------|---------------|
| `dist_matrix_type` | `str`        | Distance metric used to calculate the distance matrix. Options: `euclidean`, `cosine`, `cityblock`. | `"euclidean"` |
| `clusters`         | `str` or `int` | Defines how to determine the number of clusters. Options: `"elbow"`, `"silhouette"`, or an integer from 1 to 20. | `"elbow"`     |
| `clust_method`     | `str`        | Clustering algorithm to be used. Options: `"ward"`, `"single"`, `"complete"`, `"average"`, `"centroid"`, `"median"`, `"weighted"`. | `"ward"`      |
| `target_column`    | `str`        | Name of a specific column from the CSV to focus on for analysis.                               | `null`        |
| `list_column`      | `list`       | List of column names (features) from the CSV file to include in the clustering analysis.       | `null`        |

---

## How to Run

To run the workflow using **default settings** in `env.yaml`:

```bash
ploomber build
```

To **override** parameters from the terminal:
```bash
ploomber build --env--target_column 'ecoh' --env--list_column "['ecoh','Vm','CED']"
```