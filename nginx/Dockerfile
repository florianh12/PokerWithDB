# https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/ 


FROM nginx:1.25.0

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY ./ssl.cert /etc/nginx
COPY ./ssl.key /etc/nginx

CMD ["nginx", "-g", "daemon off;"]