#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "No argument provided. Use 'build', 'up', 'down', or 'connect'."
  exit 1
fi

# Default port
PORT=2000

# Check if a second argument (port) is provided for the build command
if [ "$1" == "build" ] && [ -n "$2" ]; then
  PORT="$2"
fi

# Perform action based on the argument
case "$1" in
  build)
    echo "Building Docker image 'inheritance' with port $PORT..."
    docker build --build-arg PORT=$PORT -t inheritance .
    ;;
  up)
    echo "Starting Docker container 'inheritance_dev'..."
    docker run -it --name inheritance_dev -p $PORT:$PORT -v $(pwd):/inheritance inheritance
    ;;
  down)
    echo "Stopping and removing Docker container 'inheritance_dev'..."
    docker stop inheritance_dev
    docker rm inheritance_dev
    ;;
  connect)
    echo "Connecting to Docker container 'inheritance_dev'..."
    docker exec -it inheritance_dev /bin/bash
    ;;
  *)
    echo "Invalid argument. Use 'build', 'up', 'down', or 'connect'."
    exit 1
    ;;
esac