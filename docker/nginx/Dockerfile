FROM nginx:1.19.0-alpine
LABEL maintainer="desh"

RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/nginx/nginx_prod.conf /etc/nginx/nginx.conf
COPY ./config/nginx/sid_prod.conf /etc/nginx/conf.d/

ARG PROJ_ROOT
ENV PROJ_ROOT=$PROJ_ROOT

VOLUME  ["/sid/"]

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]