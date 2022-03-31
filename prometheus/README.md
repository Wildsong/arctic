# arctic/prometheus

The docker-compose.yml file will create volumes that are needed
the first time it is run.

   docker-compose up

## Volumes

There might be more later, presently we have

* prometheus_config - config files
* prometheus_grafana_conf - config files
* prometheus_grafana_data - grafana.db file and plugins/ are persisted here

## Access

Prometheus is at http://yourhost:9090/

Grafana is at http://yourhost:3000/

### Credentials

Prometheus -
Grafana - use admin/admin and set a new password.

## Resources

### Prometheus

Docs
https://prometheus.io/docs/prometheus/latest/getting_started/

Book (in Safari) Prometheus: Up and Running

### Grafana

Basic docs https://grafana.com/docs/grafana/latest

Docker config 
https://grafana.com/docs/grafana/latest/installation/configure-docker/
Okay, Docker is great but I am also using a conda environment for local testing.

```bash
conda create arctic
conda activate arctic
conda install --file=requirements.txt
```

This project is not reliant on ArcGIS Pro, so if you have AGP installed and it instructs you to clone the AGP environment, DON'T. You can update instead.
```bash
conda update --all
```
