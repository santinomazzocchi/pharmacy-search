# Pharmacy-search

## Requirements
* Python3.6
* pip install json-rpc=1.13.0 - JSON-RPC transport implementation
* pip install pymongo=3.10.1 - Python driver for MongoDB
* pip install requests=2.22.0 - Python HTTP
* pip install flask=1.1.1 - A simple framework for building complex web applications
* MongoDB 3.6.3 - Database Server

# How to start this application
1. Start MongoDB database on default port: `mongod`
1. Run python application: `python3.6 app.py`
1. Run http client:
    ```
    curl \
    -H "Content-Type: application/json" \
    -X POST \
    -d '{"id": 1, "jsonrpc": "2.0", "method": "SearchNearestPharmacy", "params": { "currentLocation": {"latitude": 41.10938993,"longitude": 15.0321010},"range": 5000,"limit": 2}}' http://localhost:5000/
    ```

# How to build and run with docker
1. Compose the application `docker-compose --project-name pharmacy-search -f docker-compose.yml up --build -d`
1. Run docker: `docker-compose run web`
