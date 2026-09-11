FROM node:22-alpine AS build
WORKDIR /app
COPY React/package*.json ./
RUN npm ci
COPY React/ .
RUN npm run build

FROM nginx:alpine
COPY nginx/Frontend_ngnix.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
