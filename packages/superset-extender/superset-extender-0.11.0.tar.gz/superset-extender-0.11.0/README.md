<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Superset Extender

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![build status](https://gitlab.com/rework-space.com/apache-superset/superset-extender/badges/main/pipeline.svg)](https://gitlab.com/rework-space.com/apache-superset/superset-extender/-/jobs)

An Apache-Superset extension app that enhances it with tagging, workspaces, batch cleaning.

[**Why Superset Extender?**](#why-superset-extender) |
[**Supported Databases**](#supported-databases) |
[**Installation and Configuration**](#installation-and-configuration) |
[**Contributor Guide**](#contributor-guide) |
[**Getting started**](#getting-started) |

## Why Superset Extender?

The Superset-Extender provides:

- A **batch cleaner app** to remove entities on Apache-Superset based on predefined criteria
- An easy integration with **Apache-Airflow** for scheduled actions
- A **no-code interface** for tagging, categorizing Apache-Superset entities into workspaces
- A web-based interface for interacting with the Apache Superset API
- A **CLI**

## Screenshots

**Get a better view of superset dashboards**

<kbd><img title="Dashboards" src="https://gitlab.com/rework-space.com/apache-superset/superset-extender/-/raw/main/superset_extender/static/img/demo/superset-extender-dashboards.png"/></kbd><br/>

**Add and remove tags**

<kbd><img title="Tags" src="https://gitlab.com/rework-space.com/apache-superset/superset-extender/-/raw/main/superset_extender/static/img/demo/superset-extension-tags.png"/></kbd><br/>

**Support for categorization**

<kbd><img title="Workspaces" src="https://gitlab.com/rework-space.com/apache-superset/superset-extender/-/raw/main/superset_extender/static/img/demo/superset-extender-demo.png"/></kbd><br/>



## Supported Databases

Superset-extender can save deleted entities on any SQL-speaking datastore that has a Python DB-API driver and a SQLAlchemy dialect.

## Contributor Guide

Interested in contributing? 
Check out our [CONTRIBUTING.md](CONTRIBUTING.md)
to find resources around contributing along with a detailed guide on
how to set up a development environment.

## Getting started

- **Using pip**
```bash
# Install Superset-Extender in editable (development) mode
$ pip install supextend

# View help
$ supextend --help

# Run migrations (default database: )
$ supextend  db  upgrade 

# Initialize with data from superset
$ supextend  init

# Start the Flask dev web server from inside your virtualenv
$ supextend  run

# View charts and dashboards on superset
$ supextend  report-superset

# Remove superset charts and/or dashboards
$ supextend  clean-superset
```