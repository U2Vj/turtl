FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM nginxinc/nginx-unprivileged:alpine
COPY --from=build --chown=101:101 --chmod=555 /app/dist /srv/turtl/web
