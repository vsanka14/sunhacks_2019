# Python Flask backend
# multi-stage dockerfile

# ============================================ BASE ================================================

# Base python image, format {image:version}
ARG pythonVersion
FROM python:${pythonVersion}-slim-stretch AS base

# Set author for this docker image when pushed to registry
LABEL maintainer="amakovie@asu.edu"

# Docker build environment variables for versioning
ARG pipVersion
ARG nodeVersion

# Installs nodejs
RUN apt-get update
RUN apt-get install -y curl
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV NVM_DIR /root/.nvm
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
RUN source ${NVM_DIR}/nvm.sh \
    && nvm install ${nodeVersion} \
    && nvm alias default ${nodeVersion} \
    && nvm use default
RUN apt-get remove -y curl
ENV NODE_PATH ${NVM_DIR}/v$${nodeVersion}/lib/node_modules
ENV PATH ${NVM_DIR}/versions/node/v${nodeVersion}/bin:$PATH

WORKDIR /app

# Makes use of docker cache by copying node dependencies to the image
COPY [ "assets", "package.json", "webpack.config.js", "./"]

# Perform an `npm install`
RUN npm install

# Installs pip with proper version
RUN pip install --upgrade pip==${pipVersion}

# Makes use of docker cache by copying flask requirements to the image
COPY ./requirements requirements

# ====================================== DEVELOPMENT ===============================================

# Build stage for development extends base
FROM base AS development

# Installs the flask development requirements using pip on the image
RUN pip3 install -r requirements/dev.txt

# Copies codebase onto image
COPY . /app

# Expose port 2992 for webpack
EXPOSE 2992

# Expose port 5000 to host for flask app
EXPOSE 5000

# Tells the docker image that the flask dev server start script should run when the image runs
ENTRYPOINT .docker/start-server-postgres.sh --host=0.0.0.0

# ====================================== PRODUCTION ===============================================

# Build stage for production extends base
FROM base AS production

# Installs the flask production requirements using pip on the image
RUN pip3 install -r requirements/prod.txt

# Copies codebase onto image
COPY . /app

# Expose port 2992 for webpack
EXPOSE 2992

# Expose port 5000 to host for flask app
EXPOSE 5000

# Tells the docker image that the flask server start script should run when the image runs
ENTRYPOINT .docker/start-server-postgres.sh --host=0.0.0.0