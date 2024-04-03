FROM node:alpine as build-stage
WORKDIR /web_ui
COPY webui/proximity_web/package*.json ./
RUN npm install
COPY web_ui/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build-stage web_ui/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

