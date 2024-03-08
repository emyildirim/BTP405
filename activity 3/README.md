
  

# Note API

  

## Description:

  

This project is a RESTful API made using Python that serves as the backend for a simple note-taking application.

  
  

**About the API:**

- Programming Language: Python

- Database: MySQL

- Version Control: Git

- Containerization: Docker

- API Testing: Postman or curl

## Setup and Run

Make sure your [Python](https://www.python.org/downloads/release/python-3122/) and [Docker](https://docs.docker.com/engine/install/) are up-to-date.

The additional python packages used:
+ [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) for connecting MySQL and Python API
+ [python-dotenv](https://pypi.org/project/python-dotenv/) for using environment variables.




### Database Setup

You may want to change password  in the environment file (.env) but do not forget to change the env password in compose file. (optional)

  

### Run

Compose two containers and create the images and containers together:

```

docker-compose up

```

> Important:

> Wait for Docker to complete the compose.

  
  
  

## Endpoints

| Method | Endpoint| Description| Request Body (JSON)| Example Response |
| --- | --- | --- | --- | ---|
| GET| /notes| Returns all the notes.| N/A | [[1,"Ex Title", "Ex Content"],[2,"Ex2 Title", "Ex2 Content"]...] |
| POST | /notes | Creates a new note using the body of the request. | { "title": "Note Title", "content": "Note Content" } | Success: Note created|
| GET | /notes/:id | Returns a note with the specified id| N/A                                          | [{id},"Ex Title", "Ex Content"] |
| PUT | /notes/:id| Updates the note by id using the body of the request. | { "title": "Updated Title", "content": "Updated Content" } | Success: Note with ID [id] updated |
| DELETE| /notes/:id| Deletes the note by id.| N/A                                          | Success: Note with ID [id] deleted |
