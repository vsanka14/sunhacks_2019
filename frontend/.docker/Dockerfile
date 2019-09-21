# Vue.js frontend
# multi-stage dockerfile

# ============================================ BASE ================================================

# Base node image, format {image:version}
ARG nodeVersion
FROM node:${nodeVersion}-alpine AS base

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory
COPY . .

# ====================================== DEVELOPMENT ===============================================

# Build stage for development extends base
FROM base AS development

EXPOSE 8080

CMD [ "npm", "run", "serve" ]

# ====================================== MINIFICATION ==============================================

# Build stage for minification extends base
FROM base AS minification

RUN npm run build

# ====================================== PRODUCTION ================================================

# Production stage will use nginx for serving
FROM nginx:stable-alpine as production

# Copy the app data from minification
COPY --from=minification /app/dist /usr/share/nginx/html

EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]