# Based on the official docker guide: https://docs.docker.com/guides/vuejs/containerize
# Stage 1: Build the Vue.js

FROM node:24-alpine AS builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./

RUN --mount=type=cache,target=/root/.npm npm ci

COPY frontend/. .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginxinc/nginx-unprivileged:alpine3.23-perl AS runner

COPY deploy/frontend/nginx.conf /etc/nginx/nginx.conf

COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

USER nginx

EXPOSE 8080

ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]