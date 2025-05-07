# Personal Health Record (PHR) System API

## Description:
The design is built using microservice architecture to maximize scalability and create a maintainable system environment. Each microservice can handle a specific feature and role such as data storage, data sharing, authentication. The architecture also allows faster development cycle while using agile methodologies.
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/f268bbec-9155-43d5-8b2b-e1622760cb52" />

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
| Method | Endpoint | Description | Request Body (JSON) | Ex. Response |
|--------|----------|-------------|---------------------|--------------|
| GET | /login | Authenticates a user | {"email": "name@gmail.com", "password": "pass"} | {"message": "login successful", "token": "<token>"} |
| GET | /profile | Returns your profile info | N/A | {fullname, contact, email} |
| GET | /users | Returns all the users | N/A | [{user_id, type_id, fullname, contact, email}] |
| GET | /healthcare | Returns all healthcare providers | N/A | [{provider_id, provider_name, provider_address, provider_contact}] |
| GET | /healthcare/me | Returns the user's healthcare provider | N/A | {provider_id, provider_name, provider_address, provider_contact} |
| GET | /health_records | Returns all health records | N/A | [{record_id, user_id, record_date, record_text}] |
| GET | /health_records/:id | Returns a specific health record | N/A | {record_id, user_id, record_date, record_text} |
| GET | /permissions | Returns all the permissions | N/A | [{resource_id, type_id, can_add, can_view, can_edit}] |
| GET | /reminders | Returns all reminders | N/A | [{reminder_id, user_id, reminder_text, reminder_date}] |
| GET | /reminders/due | Returns all due reminders | N/A | [{reminder_id, user_id, reminder_text, reminder_date}] |
| GET | /reminders/:id | Returns a specific reminder | N/A | {reminder_id, user_id, reminder_text, reminder_date} |
| POST | /register | Creates a new user | {"type_id": 3, "fullname": "Name Surname", "contact": "1234567890","email": "newuser@example.com", "password": "newpass"} | {"message": "user created successfully", "token": "<token>"} |
| POST | /health_records | Creates a new health record | {"record_text": "New record"} | {"message": "health record created successfully"} |
| POST | /reminders | Creates a new reminder | {"reminder_text": "New reminder", "reminder_date": "2023-02-10"} | {"message": "reminder created successfully"} |
| POST | /healthcare | Creates a new healthcare provider | {"provider_name": "New Provider", "provider_address": "New Address", "provider_contact": "New Contact"} | {"message": "healthcare provider created successfully"} |
| PUT | /profile | Updates your profile | {"fullname": "John Doe Updated", "contact": "987-654-3210"} | {"message": "profile updated successfully"} |
| PUT | /health_records/:id | Updates a specific health record | {"record_text": "Updated record"} | {"message": "health record updated successfully"} |
| PUT | /reminders/:id | Updates a specific reminder | {"reminder_text": "Updated reminder", "reminder_date": "2023-03-10"} | {"message": "reminder updated successfully"} |
| PUT | /permissions/:id1/:id2 | Updates a specific permission | {"can_add": true, "can_view": true, "can_edit": false} | {"message": "permission updated successfully"} |
| DELETE | /health_records/:id | Deletes a specific health record | N/A | {"message": "health record deleted successfully"} |
| DELETE | /reminders/:id | Deletes a specific reminder | N/A | {"message": "reminder deleted successfully"} |
| DELETE | /users/:id | Deletes a specific user | N/A | {"message":"user deleted successfully"} |
