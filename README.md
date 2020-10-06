# The_Mentor_FLASK
This API uses HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. 

All responses come in standard JSON with [Jsend format](https://github.com/omniti-labs/jsend)

All requests must include a `content-type` of `application/json` and the body must be valid JSON.

## Response Codes 
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
	status : "success",
	data : {}
}
```
### Example Fail Message
```json
http code 422
{
	status : "fail",
	data : {"password": "Password does not match schema"}
}
```

## Register
**You send:**  Your  user info. (Password should be min 8, max 100 characters with uppercase, lowercase, number without spacing) 
**You get:**  A success or fail response

**Request:**
```json
POST /register HTTP/1.1
Accept: application/json
Content-Type: application/json
{
	"id" : "mentor1",
	"password" : "Password1234",
	"email" : "mentor1@naver.com",
	"name" : "Dongkyun Kim",
	"userType" : "mentor",
	"phone" : "01092812079",
	"birthday" :"2000-08-13",
	"location" : "seoul",
	"data" : {}
}
```

## Login
**You send:**  Your  login credentials.
**You get:**  A success or fail response

**Request:**
```json
POST /login HTTP/1.1
Accept: application/json
Content-Type: application/json
{
	"email" : "mentor1@naver.com",
	"password" : "Password1234"
}
``` 

## Logout
**You send:**  
**You get:**  A success or fail response

**Request:**
```json
POST /login HTTP/1.1
Accept: application/json
Content-Type: application/json
{
	"email" : "mentor1@naver.com",
	"password" : "Password1234"
}
``` 
