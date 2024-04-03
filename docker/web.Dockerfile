FROM node:18-alpine AS build

WORKDIR /web_ui

COPY package.json web_ui/

COPY package-lock.json web_ui/

COPY public/ web_ui/public

COPY src/ web_ui/src

RUN npm install

CMD ["npm", "run", "build"]



# NGINX
FROM nginx:alpine

WORKDIR /var/www/html

COPY --from=build /build/build/ /usr/share/nginx/html
