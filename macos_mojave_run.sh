#!/bin/bash

#  macos_mojave_run.sh
#  
#
#  Created by George Sakellariou on 20/12/2018.
#
echo "Checking if Xquartz exists....."
check_xquartz=$(which xquartz)
if [ -n "$check_xquartz" ]
then
echo "Xquartz is already installed:"
    echo $check_xquartz
else
    echo "Xquartz is going to be installed"
    brew cask install xquartz
fi
defaults write org.macosforge.xquartz.X11.plist nolisten_tcp 0
echo "Opening Xquartz...."
open -a XQuartz
ip=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')
xhost + $ip
echo "Building docker image...."
docker build -t stix_editor_image .
echo "Running docker image...."
docker run -v /:/host_filesystem/ --net=host -e DISPLAY=$ip:0 stix_editor_image
