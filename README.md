# `minnesota-bmsb-analysis`: Minnesota BMSB Analysis Pipeline

![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/lukezaruba/minnesota-bmsb-analysis)
![Swagger Validator](https://img.shields.io/swagger/valid/3.0?specUrl=https://minnesota-bmsb-analysis-phdjlv4gpa-uc.a.run.app/api/v1/swagger.json)
![GitHub last commit](https://img.shields.io/github/last-commit/lukezaruba/minnesota-bmsb-analysis)
![GitHub language count](https://img.shields.io/github/languages/count/lukezaruba/minnesota-bmsb-analysis)

An end-to-end analysis pipeline that assesses Brown Marmorated Stink Bug (BMSB) transmission risk across Minnesota. Final project for GIS 5572 (ArcGIS/Spatial Data Science II at the University of Minnesota).

## About
This repo hosts an end-to-end pipeline, to process input data, perform analytics, and serve the results out via an API. The workflow makes use of several popular Python libraries, like ArcPy, pandas, psycopg2, and Flask.


## Structure
* Datasets: `/data`

* Dockerfile for deploying API: `/docker`

* Notebooks containing implementation of analysis: `/notebooks`

* Resources: `/res`

* Source code: `/bmsb`

* Miscellaneous tools: `/tools`

## Contributors
Luke Zaruba
<br>
Mattie Gisselbeck
