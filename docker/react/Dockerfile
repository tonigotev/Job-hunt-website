# Stage 1: Build React App
FROM node:18 AS builder
WORKDIR /app
COPY package.json ./
# Force a fresh install from package.json, ignoring any lock file.
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:1.21-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
