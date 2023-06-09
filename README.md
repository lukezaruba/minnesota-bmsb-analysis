# `minnesota-bmsb-analysis`: Minnesota BMSB Analysis Pipeline

![Swagger Validator](https://img.shields.io/swagger/valid/3.0?specUrl=https://minnesota-bmsb-analysis-phdjlv4gpa-uc.a.run.app/api/v1/swagger.json)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
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
