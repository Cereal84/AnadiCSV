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

# It would be nice to be able to chose where to install the script
# Default can still be $HOME/local/bin to avoid using sudo
DEST_PATH=$HOME/.local/bin

# copy anadi.sh to $DEST_PATH
cp anadi.sh $DEST_PATH/anandi

echo "Now you can use the command '$DEST_PATH/anandi'"

echo "Please consider adding '$DEST_PATH' to your PATH environment variable"
