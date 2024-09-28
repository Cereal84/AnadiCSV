#!/bin/bash

# This script must be copied into /usr/local/bin directory

# CONF directory depends on environment variable ANADI_SETTINGS_DIR and from option 'c'
CONF_PATH="${HOME}/.config/anadi/"
# DATA directory is set by default as the current directory, iot can be changed using option 'd'
DATA_PATH=$(pwd)


ENGINE=""

function help()
{
   # Display Help
   echo "Anadi."
   echo
   echo "Syntax: anadi [-c|h|d]"
   echo "options:"
   echo "h         Print this Help."
   echo "c  PATH   Specify the settings file location."
   echo "d  PATH   Specify the data location. The default is the current directory."
   echo
}

function get_container_engine() {

    # Check if docker is running
    if docker version >/dev/null 2>&1; then
        ENGINE="docker"
    elif podman version >/dev/null 2>&1; then
        ENGINE="podman"
    else
        echo "Docker or Podman seems not to be installed or running !";
        exit 1
    fi
}


# if the env var exists use its value
if [ ! -z "${ANADI_SETTINGS_DIR}" ]; then
    CONF_PATH="${ANADI_SETTINGS_DIR}"
fi


# Get the options
while getopts "c:d:h" option; do
   case $option in
      h) # display Help
         help
         exit;;
      c) CONF_PATH=$OPTARG;;
      d) DATA_PATH=$OPTARG;;
   esac
done


get_container_engine

# check if the image exists TODO


if [ -z "$CONF_PATH" ]; then
    echo "Settings path is missing. Please use '-c' option or set the env var 'ANADI_SETTINGS_DIR'"
    exit 1
fi

# check if CONF directory exists
if [ ! -d "$CONF_PATH" ]; then
    echo "The settings directory '${CONF_PATH}' does not exists."
    exit 1
fi

# check if DATA directory exists
if [ ! -d "$DATA_PATH" ]; then
    echo "The data directory '$DATA_PATH' does not exists."
    exit 1
fi

if [ "$ENGINE" = "docker" ]; then
    docker run -it -v "$CONF_PATH":/root/.config/anadi -v "$DATA_PATH":/data/ anadi:latest
else
    podman run -it -v "$CONF_PATH":/root/.config/anadi:z -v "$DATA_PATH":/data/ anadi:latest

fi
