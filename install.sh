#!/bin/bash

# --- Includes
. scripts/utils.sh

# --- Variables

CONF_PATH="${HOME}/.config/anadi/"
BIN_DESTINATION_PATH="$HOME"
OS=""


# makes some checks and set ENGINE variable
check_requirements

case "$OSTYPE" in
  darwin*)  OS="OSX" ;; 
  linux*)   OS="Linux" ;;
  *)        echo "OS: ${Red}unknown $OSTYPE${NC}"; exit 1 ;;
esac

echo -e "OS: ${Green}${OS}${NC}" 

build_image $OS $ENGINE

# create the config directory if needed
if [ ! -d "$CONF_PATH" ]; then
    mkdir -p $CONF_PATH
fi

# copy anadi.sh in $HOME/bin as anadi
cp anadi.sh /usr/local/bin/anadi

echo "Now you can use the command 'anadi'"
