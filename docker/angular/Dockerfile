FROM node:12.2.0
LABEL maintainer="desh"

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# ENV http_proxy http://proxy.local:8080
# ENV https_proxy http://proxy.local:8080

VOLUME  ["/sid/"]
WORKDIR /sid/src/angular/ng-sid/

# install and cache app dependencies
# COPY package.json /app/package.json
RUN npm install
# RUN npm install -g @angular/cli@9
RUN npm install -g @angular/cli@9 @angular-devkit/build-angular && npm install

# add app
# COPY . /app

ARG PROJ_ROOT
ENV PROJ_ROOT=$PROJ_ROOT
ENV PATH /ng-sid/node_modules/.bin:$PATH


# RUN ng new ng-sid
# start app

# RUN ng add @angular/material
# RUN npm install moment --save
# RUN ng add @angular/material
# RUN npm install --save @covalent/core
# RUN npm install moment --save
# RUN npm i @angular/material-moment-adapter

EXPOSE 4200

#CMD ng serve --host 0.0.0.0
COPY ./angular/entrypoint.sh /entrypoint.sh

#CMD ["npm", "start"]
# CMD ng build --watch
# CMD ng serve --port 4200 --host 0.0.0.0 --proxy-config proxy.conf.json
CMD ["sh", "/entrypoint.sh"]
