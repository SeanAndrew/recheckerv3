# Rechecker V3

## The modular FastAPI SRE microservice

This application is designed to be plug and play as far as functionality, in back, core, and, front end. 
As you see it now it is used to monitor a list of domains for both DNS and HTTP resposiveness.

### prereqs
- docker
- docker-compose

TODO kubernetes setup

### Overview
There are three main components to this application:

- backend
- core
- frontend

There is also two databases with mock data for testing purposes

- mysql
- mongodb

Each of these components have docker-compose files to get you started. Those are located under the ```/ymls``` directory

You will need to create a shared docker network in order for each component to work with each other

```
docker network create shared
```
After doing so you can add a container to that shared network by adding the following to your docker compose file

```
### add to each service/container definition    
    networks:
      - shared

### towards the bottom
networks:
  shared:
    external:
      name: shared
```
### The backend contains 4 apis, and 2 schedulers
TODO primarily need to finish rewriting all of the apis here
1. ```schedule_db_sync``` triggers the ```query_db``` and runs a for each loop against ```add_new```
   1. ```query_db``` queries against the mysql database, gathers and returns a list to the scheduler
   2. ```add_new``` adds a new entry into mongodb
2. ```schedule_db_check``` triggers ```check_db``` which returns any diffs in mysql and mongodb and forwards those diffs to ```delete_old``` to remove them
   1. ```check_db``` cross compares against data in mysql and mongodb and if it finds the domain has been removed from mysql returns the domain to the scheduler
   2. ```delete_old``` removes old/decomm domains from mongodb
<br /><br />
#### Huge shout out to praveen for plugging everything below together and making it fully functional

### The core contains 3 apis, and 1 scheduler
1. ```schedule_healthcheck_sync``` triggers ```endpoint``` to fetch the current list of domains, which the scheduler than iterates over to ```http``` and ```dns```
   1. ```endpoint``` queries for the current list of data in mongodb and returns it to the scheduler
   2. ```http``` checks the domain for its current http status code. If it's in a failed state it logs and reports on the error
   3. ```dns``` checks the domain for its current dns resolution state. If it's in a failed state it logs and reports on the error

### The frontend contains 1 flask webapp
1. ```flask_web``` is the front end dashboard that feeds off the ```status``` collection in mongodb
<br /><br />
## Service Map
![Alt text](service-map.png?raw=true "Application archecture V3")

