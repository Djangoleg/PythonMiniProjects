#!/bin/sh

# Create pod.
podman pod create --name homeservicepod -p 8004:8004 -p 6379:6379

# Build home_services image.
podman build -t home_services --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z ./home_services

# Create container and add home_services to homeservicepod. --restart=always
podman create --pod homeservicepod --name home_services --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z home_services

# Build redis image.
podman build -t home_services_redis --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/redis:/usr/local/redisdata:z ./redis

# Create container and add home_services_redis to homeservicepod. --restart=always
podman create --pod homeservicepod --name home_services_redis --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/redis:/usr/local/redisdata home_services_redis

# Build home_services_celery image.
podman build -t home_services_celery --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z ./celery

# Create container and add home_services_celery to homeservicepod. --restart=always
podman create --pod homeservicepod --name home_services_celery --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z home_services_celery

# Build home_services_celery_beat image.
podman build -t home_services_celery_beat --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z ./celery_beat

# Create container and add home_services_celery_beat to homeservicepod. --restart=always
podman create --pod homeservicepod --name home_services_celery_beat --volume /home/ok/Documents/Development/Git/PythonMiniProjects/fast_api_project/hs_root/home_services:/usr/local/home_services:z home_services_celery_beat

# Start POD.
podman pod start homeservicepod


# Delete POD with containers.
# podman pod rm homeservicepod

# # Delete containers.
# podman rm home_services_celery_beat
# podman rm home_services_celery
# podman rm home_services_redis
# podman rm home_services

# Delete images.
# podman rmi home_services_celery_beat && \
# podman rmi home_services_celery && \
# podman rmi home_services_redis && \
# podman rmi home_services

# chmod +x run_home_services.sh
# Check http://localhost:8004/docs
