# Summit Technology Group (STG) Python Assignment

To build a Python application to do health check of multiple web-services

## Pre-requisites

1. Python 3
2. Docker

## Setup

Run the below command to build and launch the docker containers in the background:

```shell
$ docker-compose up --build --detach
```

Firstly you need to launch the docker containers to start 3 different web-services running on localhost:

1. Service 1 is running on Port `5001` --> http://localhost:5001/
2. Service 2 is running on Port `5002` --> http://localhost:5002/
3. Service 3 is running on Port `5003` --> http://localhost:5003/

All services have a single endpoint - `/health` which returns a JSON:

    http://localhost:500X/health

```json
{
    "status": bool (true / false)
}
```

## Task submission

To submit the assignment, please create a private GitHub repo and share the access with:

  - `GoelJatin`
  - `dennijo`

We expect this shouldn’t take more than 24 hours so it would be great if you could share the submission at the earliest.

## Task description

1. The Python application should take the list of service URLs as a JSON config input
2. Call the `/health` endpoint of each service exactly `10000` times
3. Maintain counter for success and failure of each response per service
4. After completing the operation for each service return a single output of status per service, such as,
    ```json
    {
        "service1": {
            "success": num_success,
            "failure": num_failure,
            "min_response_time": ,
            "max_response_time": ,
            "mean_response_time":
        },
        "service2": {
            "success": num_success,
            "failure": num_failure,
            "min_response_time": ,
            "max_response_time": ,
            "mean_response_time":
        },
        "service3": {
            "success": num_success,
            "failure": num_failure,
            "min_response_time": ,
            "max_response_time": ,
            "mean_response_time":
        }
    }
    ```
    **where num_success + num_failure should equal to 10000**

### Key points

1. You should define a class for maintaining the connection to each service, i.e., instead of calling the API directly using `requests.get(url)` in the application code, you should have a class structure and class would have the url details and then a method to call the `/health` endpoint, which would get the url internally
2. There should be **one and only one class instance for each service**
3. Implement LOGGING in the application


**BONUS Points** on providing statistics on the response time
