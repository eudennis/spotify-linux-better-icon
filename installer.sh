#!/bin/bash

VERSION=$(lsb_release -r -s)
DISTRO=$(lsb_release -i -s)
PROGRAM=$(desktop-file-install)
OPTIONS="Yes No"

if [ "$PROGRAM" != "Must specify one or more desktop files to process." ]; then
  echo "desktop-file-install not available. This script will fail. Exiting..."
  exit
fi
echo "Detected desktop-file-install. Good!"
if [ "$DISTRO" != "Ubuntu" ] && ["$VERSION" < 11.04 ]; then
	echo "Detected wrong distro or version. Please read the readme. Exiting..."
	exit
fi
echo "Detected Ubuntu Version $VERSION, this should work. Hold on!"
echo "-----"
echo "This script only makes *basic* checks for distribution, version, and software to make sure it will succeed. By continuing, you understand that this script will only work on Ubuntu versions using the Unity GUI, and that any issues it may otherwise cause are your fault. It has only been tested on 12.04+. Do you want to continue?"


select opt in $OPTIONS; do
  if [ "$opt" = "Yes" ]; then
    desktop-file-install spotify.desktop
  elif [ "$opt" = "No" ]; then
    echo "Exiting..."
    exit
  else
    echo "Bad Option. Exiting..."
    exit
  fi
done


