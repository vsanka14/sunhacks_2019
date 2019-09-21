#!/bin/bash

# Run npm command to bootstrap the environment
npm start

# Start webpack and flask servers
npm run build
flask run $1