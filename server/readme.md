# How to run
1. Enter to clientServer directory
2. please enter virtual env -> . server/venv/bin/activate
3. then run the server -> python server/app.py


# How to generate the file
1. please prepare your client application
2. send this json by using POST method to http://127.0.0.1:8080/api

{
    "type": "generate",
    "version": "1.0",
    "param": {},
    "uuid": "24c4ccf2-a587-4f84-b6db-fdca7b360e07"
}

3. You will get this response

{
    "type": "generate",
    "version": "1.0",
    "param": {
        "link": "/home/febry/clientServer/server/randomData.txt"
    },
    "requestUuid": "24c4ccf2-a587-4f84-b6db-fdca7b360e07"
}

# How to get the report
1. please prepare your client application
2. send this json by using GET method to http://127.0.0.1:8080/api

{
    "type": "report",
    "version": "1.0",
    "param": {
        "link": "/home/febry/backendFlask/randomData.txt"
    },
    "uuid": "e0646fd8-5f84-4203-bf45-0844fad94e2d"
}

3. You will get this response

{
    "type": "report",
    "version": "1.0",
    "param": {
        "link": "/home/febry/backendFlask/randomData.txt",
        "alphabetical strings": 25465,
        "integers": 23472,
        "real numbers": 23477,
        "alphanumerics": 20547
    },
    "requestUuid": "e0646fd8-5f84-4203-bf45-0844fad94e2d"
}