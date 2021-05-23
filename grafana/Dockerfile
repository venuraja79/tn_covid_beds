FROM grafana/grafana
ENV GF_INSTALL_PLUGINS grafana-worldmap-panel,marcusolsson-csv-datasource,grafana-simple-json-datasource
ADD heroku-run.sh /
ADD grafana.ini /etc/grafana/grafana.ini
ADD tn_covid_beds.csv /usr/share/tn_covid_beds/tn_covid_beds.csv
ADD tn_covid_district_beds.csv /usr/share/tn_covid_beds/tn_covid_district_beds.csv
ENTRYPOINT [ "/heroku-run.sh" ]