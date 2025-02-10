#!/bin/bash

case "$1" in
    build)
        shift
        docker build -t python-docker-app "$@" .
        ;;
    run|*)
        docker run -it -v $(pwd):/app -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY python-docker-app
        ;;
esac
