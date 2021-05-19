# Prerequisites
Prerequisites for SID

## Docker
Please make sure you have latest version of docker installed, for docker installation please follow instruction from
* [Get Docker](https://docs.docker.com/get-docker/)

## Git
Please make sure you have git installed on your machine
* [Git](https://git-scm.com/downloads)

# Installation Steps

## Download SID

download SID git repo

```
$ git clone https://github.com/deshk04/sid.git
```
change directory to sid and edit file .env under docker folder. update variable REPO_PATH to folder where sid repo is download. for e.g. if you downloaded SID in folder c:\download\sid
```
REPO_PATH=c:\download\sid
```

## Build SID

open terminal and change directory to docker under sid repository
for e.g.
```
$ cd c:\download\sid\docker
```
run docker build command
* for demo environment
```
$ docker-compose -f docker-compose_demo.yml build
```
* for development environment
```
$ docker-compose -f docker-compose.yml build
```
*Please dont use demo or development environment for production jobs*

## Run SID
Once build is complete without any errors you can run SID
* for demo environment
```
$ docker-compose -f docker-compose_demo.yml up
```
If you are using demo then you can access SID on port 8080 on your browser
just open http://localhost:8080/ on your browser

* for development environment
```
$ docker-compose -f docker-compose.yml up
```
If you are using development environment then you can access SID on port 4200 on your browser
just open http://localhost:4200/ on your browser

## Troubleshoot
If you are facing problem with angular build, then the following
* edit entrypoint.sh from docker/angular
* comment (add # at the begining) last line ng serve
* uncomment (remove #) while true; do sleep 2; done
* now build the container as per the above steps

Once angular container is up, connect to the connector and perform the following steps.
To enter the container
```
$ docker exec -it sid_ng_container bash
```
Once you are in angular container, try and run the build. you might want to run the following commands first
```
$ npm cache clean
```
```
$ npm install
```






