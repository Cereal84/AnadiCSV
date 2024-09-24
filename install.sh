#!/bin/bash

# build Docker image
./build_image.sh

# copy anadi.sh in $HOME/bin as anadi
cp anadi.sh "$HOME/.local/bin/anadi"

echo "Now you can use the command 'anadi'"
