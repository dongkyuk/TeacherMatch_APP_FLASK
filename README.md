# The_Mentor_FLASK
This API uses HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to indenticate status and errors. 

All responses come in standard JSON with [Jsend format](https://github.com/omniti-labs/jsend)

All requests must include a `content-type` of `application/json` and the body must be valid JSON.

## Requirements
mysql

## API Documentation
Documentation is done with [Flassger](https://github.com/flasgger/flasgger).

Flasgger comes with SwaggerUI embedded so you can access http://localhost:5000/apidocs and visualize and interact with your API resources.

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
