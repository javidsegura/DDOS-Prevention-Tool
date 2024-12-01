#!/bin/bash

# DESCRIPTION: Run a docker container with a weak application to be attacked


docker run -m 220m --memory-swap 220m \
    -p 8501:8501 \
    --add-host=host.docker.internal:host-gateway \
    --name demoweb \
    -it myapp /bin/bash 
# --add-host=host.docker.internal:host-gateway \ # For macOS only!