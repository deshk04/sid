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
## Run SID
Once build is complete without any errors you can run SID
* for demo environment
```
$ docker-compose -f docker-compose_demo.yml up
```
* for development environment
```
$ docker-compose -f docker-compose.yml up
```




