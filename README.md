# SID
Simple ETL tool for Salesforce

## What is SID?
SID is simple Data Loader environment for Salesforce. with SID you can extract data from multiple connectors and load data to Salesforce. you can also download data from Salesforce
## Why SID?
There are plenty of good ETL , data pipeline tools available which has lots more connectors then SID, then why SID? Most solutions are cloud based or very expensive, to use cloud based solution requires enterprise data to be sent via solution provider which is not always feasible due to enterprise security policies. SID allows you to setup an local data loader environment, where you can create new job, schedule job and configure you process as per your need without worry about data access to 3rd party or cloud usage cost.


## How to Guide
* [Installation](doco/install.md)
* [Create a new connector](doco/connector.md)
* [Create a new Job](doco/job.md)
* [Create a new Schedule](doco/schedule.md)
* [Run Job](doco/runjob.md)

Fresh installation requires following objects in the order
* Connectors (source and destination)
* new job which will utilise the above connectors
* schedule (optional) if you are going to run regular jobs

### To Do List
* use [Singer Protocol](https://www.singer.io/)
* support postgres and odbc databases
* support MS Dynamics