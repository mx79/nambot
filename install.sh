#!/bin/bash
#
# Script used to install all the requirements from the project.
# It can be used on your local machine if she is based on UNIX.
# This file is useful to containerize the app with the Dockerfile.

pip install -r requirements.txt
pip install pkg/*.tar.gz

exit 0
