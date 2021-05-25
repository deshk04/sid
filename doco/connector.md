# Connectors

Connectors are used for connecting to various data sources and working with their data. Connectors are used by Jobs, you are required to create source and destination connectors before you can create Jobs.

SID support following connectors
* Salesforce
* AWS S3
* Local
* Postgres (Work in progress)

## Salesforce
Salesforce Connector can be created as below
![Salesforce Connector](images/sid_new_sf_connector.png "Salesforce Connector")

OAuth is currently not supported, connector requires
* User Name
* Password
* Token
* System Type

## AWS S3
S3 Connector can be created as below
![AWS S3](images/sid_new_s3_connector.png "S3 Connector")

all fields are mandatory

## Local
SIDLocal is Local filesystem of SID (area where SID sid installed)

## Postgres
Postgres connector is currently in development