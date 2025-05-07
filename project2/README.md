
  

# Cloud-based Restaurant Reservation System

[YouTube Link](https://www.youtube.com/watch?v=T49e6Rc7B4k&t)  

## Description

  

The Cloud-based Restaurant Reservation system is designed to enable users and restaurant staff to manage reservations efficiently, all in one place. This full-stack application is hosted on the AWS cloud service through a virtual machine, leveraging a microservices architecture for enhanced scalability and maintenance. It features a RESTful API written in Python, with MySQL for database management, and utilizes Next.js and React for the user interface. Security and privacy are paramount, with JWT (JSON Web Token) ensuring encrypted communication between the client and the server.
<img width="1458" alt="image" src="https://github.com/user-attachments/assets/d4d6c787-70ac-4fb8-b844-3d44cd2c8da4" />

  

### Key Features

  

- Can be hosted on AWS and Azure cloud services.

- Utilizes JWT for secure communication.

- Supports user account creation and management.

- Offers a user-friendly interface for managing reservations.

- Sends reminders and notifications to users.

  

## Guideline (How to Use It)

  

Ensure your system has the latest versions of [Python](https://www.python.org/downloads/release/python-3122/), [Docker](https://docs.docker.com/engine/install/), and [Node](https://nodejs.org/en/download/current).

  

### Python Dependencies

  

-  `mysql-connector-python`: For connecting MySQL with the Python API. [Download](https://pypi.org/project/mysql-connector-python/)

-  `python-dotenv`: For managing environment variables. [Download](https://pypi.org/project/python-dotenv/)

-  `bcrypt`: For password hashing. [Download](https://pypi.org/project/bcrypt/)

-  `jwt`: For authorization. [Download](https://pypi.org/project/jwt/)

  

### Node Dependencies

  

-  `bootstrap`: For styling. [Download](https://www.npmjs.com/package/bootstrap)

-  `jsonwebtoken`: For authorization management. [Download](https://www.npmjs.com/package/jsonwebtoken)

-  `jwt-decode`: For decoding JWTs. [Download](https://www.npmjs.com/package/jwt-decode)

-  `react-bootstrap`: For React compatibility. [Download](https://www.npmjs.com/package/react-bootstrap)

-  `react-hook-form`: For forms and validation. [Download](https://www.npmjs.com/package/react-hook-form)

-  `swr`: For data fetching. [Download](https://www.npmjs.com/package/swr)

  
  

### Setup Environment Variables

  

go to the directory named "python", create a .env file and add the following:

```

_HOST=mysql
MYSQL_DATABASE=db
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=password
JWT_SECRET=secret

```

  

Also, go to the directory named "my-app", create a .env file and add the following:

```

NEXT_PUBLIC_API_URL=http://localhost:8080/api

```

> Important:

  

> You can modify the MYSQL_ROOT_PASSWORD, SECRET_KEY, JWT_SECRET and NEXT_PUBLIC_API_URL, also do not forget to edit the Docker compose file accordingly.

  

### Run Locally

  

Go to the .yml directory and compose two containers and create the images and containers together:

  

```

docker-compose up

```

  

> Important:

  

> Wait for Docker to complete the compose, if the MySQL connection is unhealthy just run the command again.

  

### Run on Cloud

Go to the directory named "python", open the ‘sever.js’ and add your VM Public IP address to the origins and Next.js app port to allow CORS like this:

  

```

allowed_origins = ['http://localhost:3000', 'http://<VM_PUBLIC_IP>:<NEXTJS_PORT>']

```

  

> Important:

  

> Also ensure that you have enabled your VM security to be accessible to public, set security group to ‘0.0.0.0/0’ with port number of the server (8080) and UI (3000) and attach it to your VM.

  

Open the Next.js app to public by modifying package.json:

  

```

"start": "next start -H 0.0.0.0"

```

  

Ensure that you are at the same directory as .yml and compose the tree images and create the containers together by:

  

```

docker-compose build

```

  

And then:

  

```

docker-compose up

```

  
  

## Existing Demo Users

  

Below are demo user accounts created for testing and demonstration purposes. Please note that the email addresses and passwords are fictional.

  


| User Type | Username (Email)       | Password |
|-----------|------------------------|----------|
| Customer  | johndoe@yahoo.com      | pass01   |
| Customer  | janesmith@outlook.com  | pass02   |
| Staff     | mitchel91@gmail.com    | pass03   |


  

**Warning:** The email addresses and passwords listed above are not real. They are only used for demonstration and testing purposes within the database.

  

## API Endpoints

  

The following table outlines the RESTful API endpoints available in the Cloud-based Restaurant Reservation System, including the HTTP method, endpoint, and a brief description of the endpoint's function.

  


| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| POST   | `/register`            | Creates a new user                 |
| GET    | `/login`               | Authenticates a user               |
| GET    | `/users`               | Retrieves all users                |
| GET    | `/profile`             | Retrieve your profile              |
| PUT    | `/profile`             | Updates your profile               |
| POST   | `/reservations`        | Creates a reservation              |
| GET    | `/reservations`        | Retrieves all reservations         |
| GET    | `/reservations/due`    | Retrieve all due reservations      |
| GET    | `/reservations/:id`    | Retrieves reservations by user id  |
| PUT    | `/reservation/:id`     | Updates a reservation              |
| DELETE | `/reservation/:id`     | Deletes a reservation              |
