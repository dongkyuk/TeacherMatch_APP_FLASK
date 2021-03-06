# The_Mentor_FLASK

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Structure](#structure)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [API Documentation](#api-doc)
  * [Response Codes](#response-codes)
  * [Example Success Message](#example-success-message)
  * [Example Fail Message](#example-fail-message)


<!-- ABOUT THE PROJECT -->
## About The Project
RESRful API for The Mentor App Backend.

This API uses HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. 

All responses come in standard JSON with [Jsend format](https://github.com/omniti-labs/jsend)

All requests must include a `content-type` of `application/json` and the body must be valid JSON.

### Structure
```
├── README.md               
├── The_Mentor.sql                        # SQL File for mysqldb
├── app
│   ├── MatchHandler.py                   # API Resource for match, heart, hashtag
│   ├── UserHandler.py			  # API Resource for user authentication
│   ├── database.py                       # Database init
│   ├── docs				  # Documentation folder
│   ├── messages.py                       # Response message class
│   ├── models.py			  # Models for flask-sqlalchemy
├── config.py				  # App Config
├── requirements.txt
├── run.py				  # Run app
```

### Built With
* [MySQL](https://www.mysql.com)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* MySQL
```sh
brew install mysql
```


### Installation

1. Clone the repo
```sh
git clone https://github.com/github_username/repo_name.git
```
2. Install requirements
```sh
pip install -r requirements.txt
```
3. Set up MySQL database server (create a db and run the_mentor.sql session)

[How-to](https://dev.mysql.com/doc/mysql-getting-started/en/) (Docker recommended)

4. Run
```sh
python3 run.py
```
You can still access the API structure in http://localhost:5000/apidocs without Step 3


<!-- API DOC -->
## API Documentation
Documentation is done with [Flassger](https://github.com/flasgger/flasgger).

Flasgger comes with SwaggerUI embedded so you can access http://localhost:5000/apidocs and visualize and interact with your API resources.

[![Swagger UI Screen Shot][swagger-screenshot]](http://localhost:5000/apidocs)

### Response Codes
```
200: Success
400: Bad request
401: Unauthorized
404: Cannot be found
405: Method not allowed
422: Unprocessable Entity 
50X: Server Error
```

### Example Success Message
```json
http code 200
{
	"status" : "success",
	"data" : {}
}
```
### Example Fail Message
```json
http code 422
{
	"status" : "fail",
	"data" : {"password": "Password does not match schema"}
}
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[swagger-screenshot]: image/Screenshot.png
