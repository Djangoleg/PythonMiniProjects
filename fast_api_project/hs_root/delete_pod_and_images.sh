#!/bin/sh

# Delete POD with containers.
podman pod rm homeservicepod

# Delete images.
podman rmi home_services_celery_beat
podman rmi home_services_celery
podman rmi home_services_redis
podman rmi home_services

# chmod +x delete_pod_and_images.sh

