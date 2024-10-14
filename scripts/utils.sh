#!/usr/bin/env bash

# -- colors
Red='\033[0;31m'
Green='\033[0;32m'
Yellow='\033[0;33m'
Cyan='\033[0;36m'
NC='\033[0m'

ENGINE=""

am_i_root() {

  if [ $(id -u) -ne 0 ]; then
      echo -e "${Red}ERROR:${NC} Please run as root" >&2;
      exit 1
  fi
}


check_requirements() {

    # we need super-user privileges in order to
    # copy the anadi.sh file into /usr/local/bin directory
    am_i_root

    # We neeed to have one between Docker or Podman installed.
    # We store which engine is installed in ENGINE variable

    # Check if docker is running
    if docker version >/dev/null 2>&1; then
        ENGINE="docker"
    fi

    # Check if podman is running
    if podman version >/dev/null 2>&1; then
        ENGINE="podman"
    fi

    if [ -z "$ENGINE" ]; then
        echo -e "${Red}ERROR:${NC}Docker or Podman seems not to be installed or running !";
        exit 1
    fi
}


build_image() {

    # $1 is the OS
    # $2 is the engine 'docker' or 'podman'

    os=$1
    container_engine=$2
    container_file="./Dockerfile"
    build_status="1"


    # for OSX there is no pre-compiled duckdb so we need to use a different
    # Dockerfile
    if [ "$os" = "OSX" ]; then 
        container_file="./Dockerfile_macos"
    fi

    echo -e "Engine: ${Green}${container_engine}${NC}"
    echo -e "File: ${Green}${container_file}${NC}"

    if [ "$container_engine" = "docker" ]; then

        if [ -z "$(docker images -q anadi:latest)" ]; then
            if ! docker build -f $container_file -t anadi .; then
                build_status="0"
            fi
        else
            build_status="2"
        fi
    fi


    if [ "$container_engine" = "podman" ]; then
        if [ -z "$(podman images -q anadi:latest)" ]; then
            if ! podman build -f $container_file -t anadi; then
                build_status="0"
            fi
        else
           build_status="2"
        fi
    fi

    case $build_status in
        0) echo -e "Image Build: ${Red}FAIL${NC}";;
        1) echo -e "Image Build: ${Green}SUCCESS${NC}";;
        2) echo -e "Image:  ${Yellow}Already Exists${NC}";;
    esac
}

