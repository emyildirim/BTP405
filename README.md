# Personal Health Record (PHR) System API

## Description:
The design is built using microservice architecture to maximize scalability and create a maintainable system environment. Each microservice can handle a specific feature and role such as data storage, data sharing, authentication. The architecture also allows faster development cycle while using agile methodologies.

Python RESTful API handles all the HTTP requests and connects the front-end and the database. The key features of the cloud based PHR system follows:
 
+ Self-Hosted.
+ Permissions and Security.
+ JWT (JSON Web Token).
+ Health data entry and Management.
+ Integration with healthcare providers.
+ Safe health record sharing.
+ Reminders and Alerts
 

## Setup and Run

Make sure your [Python](https://www.python.org/downloads/release/python-3122/) and [Docker](https://docs.docker.com/engine/install/) are up-to-date.

The python dependencies used:
+ [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) for connecting MySQL and Python API
+ [python-dotenv](https://pypi.org/project/python-dotenv/) for using environment variables.
+ [bcrypt](https://pypi.org/project/bcrypt/) for password hashing and storing (authentication).
+ [jwt](https://pypi.org/project/jwt/) for authorization.

### Setup Environment Variables

go to the directory named "python", create a .env file and add the following:
```
_HOST=mysql

MYSQL_DATABASE=db

MYSQL_USER=root

MYSQL_ROOT_PASSWORD=password

SECRET_KEY=secret
```
> Important:

> You can modify the MYSQL_ROOT_PASSWORD and SECRET_KEY and do not forget to edit the Docker compose file accordingly.

  

### Run

Compose two containers and create the images and containers together:

```

docker-compose up

```

> Important:

> Wait for Docker to complete the compose, if the MySQL connection is unhealthy just run the command again.

## Existing Demo Users

| User Type | Username (Email) | Password |
| --- | --- | --- |
| Admin | alice1982@yahoo.com | pass01 |
| Doctor | cahrlesh4@outlook.com | pass02 |
| Patient | mitchel91@gmail.com | pass03 |

> Warning:

> The Email or Passwords are just a representation and not real. Only used for demonstration and testing purposes in the database.
  
  
## Endpoints

