# ==================================== BASE ====================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-3.7}
FROM python:${INSTALL_PYTHON_VERSION}-slim-stretch AS base

RUN apt-get update
RUN apt-get install -y \
    curl

ARG INSTALL_NODE_VERSION=${INSTALL_NODE_VERSION:-12}
RUN curl -sL https://deb.nodesource.com/setup_${INSTALL_NODE_VERSION}.x | bash -
RUN apt-get install -y \
    nodejs \
    && apt-get -y autoclean

WORKDIR /app
COPY requirements requirements

COPY [ "assets", "package.json", "webpack.config.js", "./" ]
RUN npm install

# ================================= DEVELOPMENT ================================
FROM base AS development
RUN pip install -r requirements/dev.txt
EXPOSE 2992
EXPOSE 5000
CMD [ "npm", "start" ]

# ================================= PRODUCTION =================================
FROM base AS production
RUN pip install -r requirements/prod.txt
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]

# =================================== MANAGE ===================================
FROM base AS manage
RUN pip install -r requirements/dev.txt
ENTRYPOINT [ "flask" ]
