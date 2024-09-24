#!/bin/bash

CONF_PATH="${HOME}/.config/anadi/"


# build Docker image
./build_image.sh

# create the config directory if needed
if [ ! -d "$CONF_PATH" ]; then
    mkdir -p $CONF_PATH
fi

# copy anadi.sh in $HOME/bin as anadi
cp anadi.sh "$HOME/.local/bin/anadi"

echo "Now you can use the command 'anadi'"
