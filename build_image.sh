#!/bin/bash

# Try to build image with docker command (also work for podman-docker bindings)
docker build -t anadi . ||
echo "docker command don't work, trying with podman"
podman build -t anadi .
