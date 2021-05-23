# Using Grafana for visualization 

## Overview

This folder contains the files for using Grafana for data visualization. The current code can be used for grafana deployment in Heroku containers.

The visualization works on static data which is locally stored. Since the heroku free container shuts down after 30 minutes of inactivity the dashboard and data source details are lost.

## List of files in the folder

| File Name  | Description |
| ------------- | ------------- |
|docker-compose.yml  | To be used for local development contains grafana and python middleware which fetches data |
| Dockerfile  | Used for heroku deployment  |
| heroku.yml  | Heroky uses this file to invoke dockerfile  |
| heroku-run.sh | Used for heroku deployment and port binding  |
| TN_BED_DASH.json | Dashboard which reads data from local CSV file |
| datasource.yaml | Grafana datasource file |

## Features work in progress 

1. Dynamically add pre-configured datasource 
2. Dynamically add pre-configured dashboard 
3. Integration with fast API middleware for data fetch 

## Sample

![Alt text](./Grafana_Dashboard.png?raw=true "Sample")