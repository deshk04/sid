FROM node:12.2.0
LABEL maintainer="desh"

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# ENV http_proxy http://proxy.local:8080
# ENV https_proxy http://proxy.local:8080

RUN apt-get update && apt-get install --no-install-recommends -y \
    dos2unix \
    less

WORKDIR /app

# install and cache app dependencies
COPY ./src/angular/ng-sid/package.json /app/package.json
RUN npm install
# RUN npm install -g @angular/cli@9
# RUN npm install -g @angular/cli@9 @angular-devkit/build-angular && npm install

# add app
# COPY . /app

ARG PROJ_ROOT
ENV PROJ_ROOT=$PROJ_ROOT
ENV PATH /sid/src/angular/ng-sid/node_modules/.bin:$PATH

VOLUME  ["/sid/"]
WORKDIR /sid/src/angular/ng-sid/

EXPOSE 4200

#CMD ng serve --host 0.0.0.0
COPY ./docker/angular/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh

#CMD ["npm", "start"]
# CMD ng build --watch
# CMD ng serve --port 4200 --host 0.0.0.0 --proxy-config proxy.conf.json
CMD ["sh", "/entrypoint.sh"]
