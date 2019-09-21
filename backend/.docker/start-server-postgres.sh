#!/bin/bash

# Waits for db (postgres) to start
echo "Waiting for db to initialize and for incoming connections..."
sleep 4

# Start node and flask in background
npm run build
npm start &

# Checks for migrations folder, if doesn't exist, then initialize migrations folder
DIR=/app/migrations
if [[ ! -e $DIR ]]; then
    flask db init
fi

# Runs the flask database migration routine
flask db migrate
flask db upgrade &&
tail -f /dev/null