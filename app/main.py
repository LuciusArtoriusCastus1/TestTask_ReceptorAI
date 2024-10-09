from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from database import destinations_collection, logs_collection, strategy_collection
from jwt_conf import create_token, verify_token
from log_conf import logger
from models import Event, Destination, User
from services import get_current_strategy, apply_strategy, route_the_event

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": True},
    title="MyApp",
    description="Small router app",
    version="1.0.0",
)


@app.post("/route")
async def route_event(event: Event):  # token: dict = Depends(verify_token)
    # Endpoint for routing the event
    try:
        strategy = event.strategy or get_current_strategy()
        filtered_intents = apply_strategy(strategy, event.routingIntents)

        destinations = list(destinations_collection.find(
            {"destinationName": {"$in": [intent.destinationName for intent in filtered_intents]}}))

        for destination in destinations:
            await route_the_event(destination, event.payload)

        response = {"message": "Event routed successfully",
                    "destinations": [dest["destinationName"] for dest in destinations]}

        logs_collection.insert_one({
            "timestamp": datetime.utcnow(),
            "request": event.dict(),
            "response": response,
            # "token": token,
        })

        return response
    except Exception as e:
        logger.error(f"Error while routing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/init")
async def init_destinations():
    # Endpoint for creating some predefined destinations
    destinations = [
        {"destinationName": "destination1", "transport": "http.post", "url": "http://127.0.0.1:8000/destination1"},
        {"destinationName": "destination2", "transport": "http.post", "url": "http://127.0.0.1:8000/destination2"},
        {"destinationName": "destination3", "transport": "log.info"},
        {"destinationName": "destination4", "transport": "log.warn"},
    ]

    destinations_collection.insert_many(destinations)
    strategy_collection.insert_one({"name": "ALL", "current": True})

    return {'response': 'Initiated successfully'}


@app.post('/destination1')
async def destination1():
    # Predefined destination URL
    return {'response': 'custom_destination1'}


@app.post('/destination2')
async def destination2():
    # Predefined destination URL
    return {'response': 'custom_destination2'}


@app.post('/custom-destination')
async def create_destination(destination: Destination):
    # Endpoint for creating custom destination
    destinations_collection.insert_one(destination.dict())

    return {'response': 'Created successfully'}


@app.post('/create-jwt')
async def create_jwt(user: User, timedelta=None):
    # Endpoint for creating JWT token
    token = create_token(data=user.dict(), expires_delta=timedelta)
    return {'token': token}


@app.get('/collection/{collection_name}')
async def list_collections(collection_name: str):
    # Endpoint for tracking collections
    if collection_name == "destinations":
        data = destinations_collection.find({}, {"_id": 0})
        return {'collection': data.to_list()}
    elif collection_name == "logs":
        data = logs_collection.find({}, {"_id": 0})
        return {'collection': data.to_list()}
    else:
        return {'message': 'Invalid collection name'}
