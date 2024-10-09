# TestTask_ReceptorAI

# FastAPI Router Application

Simple router that handles incoming events and routes them to one or multiple destinations according to a routing strategy.


## Setup

1. Clone the repository:

2. Build the Docker image:
   ```
   docker build -t fastapi-router-app .
   ```

3. Start a MongoDB instance:
   ```
   docker run -d --name mongodb -p 27017:27017 mongo
   ```

4. Initialize the MongoDB with some sample data:

## Running the Application

1. Run the Docker container:
   ```
   docker run -d --name fastapi-router-app -p 8000:8000 --link mongodb:mongodb fastapi-router-app
   ```

2. The application should now be running and accessible at `http://localhost:8000` or `http://127.0.0.1:8000`.

## API Usage

First of all you can initialize some predefined destinations:
```
http://127.0.0.1:8000/init
```
or 

create your own destinations:
```
http://127.0.0.1:8000/custom-destination
```
To route an event, send a POST request to `/route` with the following JSON body:

```json
{
  "payload": {"a": 1, "b": 2, "c": 3},
  "routingIntents": [
    {"destinationName": "destination1", "important": true, "bytes": 128},
    {"destinationName": "destination2", "important": true, "bytes": 2048},
    {"destinationName": "destination3", "important": false, "bytes": 4096}
  ],
  "strategy": "IMPORTANT"
}
```

Create JWT token:
```
http://127.0.0.1:8000/create-jwt
```

and

Include a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```