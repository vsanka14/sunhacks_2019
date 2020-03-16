# Running this Vue.js / Flask app using Docker

This Vue / Flask boilerplate project provides full Docker integration for developers as well as staging and production purposes.

## Getting Started

These instructions will get you a copy of this boilerplate project up and running on a local machine running Docker for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

These tools must be installed prior to attempting to spin up this project on a local machine

```
Docker CE (Includes the Docker Engine and CLI)
https://docs.docker.com/install/
```

```
Docker Compose
https://docs.docker.com/compose/install/
```

### Stand up using Docker

Step by step on running the boilerplate in a development env using Docker.
The dockerized development env will spin up one instance each of the frontend, backend, Postgres db, and Redis cache.

Clone the repository. Change directory to the cloned project. Run this command to initialize .env file:

```
$ cp .env.example .env
```

Then run:

```
$ docker-compose up
```

The frontend will be available at:

```
http://localhost:8080/
```

The backend will be available at:

```
http://localhost:5000/
```

Use a tool such as Kitematic to monitor the status of the containers in development env.

## Push Docker images to registry

In order to increase efficiency in deploying to a development server, developer's machine, or production cluster, the frontend and backend Docker images can be pushed to a registry, such as DockerHub.

To do this, first follow all the steps above to ensure the containers function properly on one machine.
Then edit:
```
docker-compose.override.yml
```
or, for production and staging, edit:
```
production.yml, docker-compose-swarm.yml
```
and uncomment this key for both the frontend and backend service:
```
#image: fill in with frontend image tag
```
and set this key to correspond with the desired registry and tag for the image, for example:
```
image: foobar/frontend:latest
```
then build these images for development:
```
$ docker-compose build
```
or for production:
```
$ docker-compose -f production.yml build
```
then push the built / tagged images to a development registry
```
$ docker-compose push
```
or a production registry
```
$ docker-compose -f production.yml push
```

## Deployment

These instructions will assist in deploying this boilerplate to a production cluster. In this case, the primary driver for deployment is Docker Swarm.

### Prequisites

```
Docker Swarm (Running with at least one manager node)
```

### Testing production environment on local machine (staging)

After becoming familiar with how to stand up a Docker development env from the steps above, try standing up a Docker staging env using this command:
```
$ docker-compose -f production.yml up
```
This will allow for the local machine to run the Vue / Flask app with production variables for staging purposes.

Once staging is complete, one can proceed through the steps for deployment to a production cluster.

### Deploying to a Docker Swarm with an HA Postgres stack

Before deploying the Vue / Flask and cache stack to a swarm, a high-availability Postgres stack will first be deployed. This stack contains a PgPool service for load-balancing database read requests, and four Postgres instances (one acting as a master) and all synchronously replicated. 

With the repository cloned and the directory changed to newly cloned repo, ensure the command-line environment is set to a manager node in the swarm, for example:
```
$ eval $(docker-machine env node-1)
```
Then deploy the HA Postgres stack to the swarm:
```
$ docker stack deploy -c postgres-stack.yml ha-postgres
```
Ensure that the ```DATABASE_URL``` key in the ```.env``` file contains the host ```pgpool```, for example:
```
DATABASE_URL=postgresql://dev:secret@pgpool/db
```
Monitor and wait for the PgPool service to be running:
```
$ docker service ps pgpool
```
Then deploy the app and cache stack:
```
$ docker stack deploy -c docker-compose-swarm.yml vue-flask
```

The frontend and backend are then exposed to the particular endpoint established when the network administrator provisioned the swarm at:
```
http://endpoint:8080, http://endpoint:5000
```
A swarm visualizer is also available at:
```
http://endpoint:8081
`
