import logging
from typing import List, Dict, Any
import httpx
from database import strategy_collection
from log_conf import logger
from models import RoutingIntent


def get_current_strategy():
    # Method for getting current strategy from the database
    strategy = strategy_collection.find_one({"current": True})
    return strategy["name"] if strategy else "ALL"


def apply_strategy(strategy: str, routing_intents: List[RoutingIntent]):
    # Method that returns a list of strategies by the specified routing intent
    if strategy == "ALL":
        return routing_intents
    elif strategy == "IMPORTANT":
        return [intent for intent in routing_intents if intent.important]
    elif strategy == "SMALL":
        return [intent for intent in routing_intents if intent.bytes < 1024]
    elif strategy.startswith("lambda"):
        custom_strategy = eval(strategy)
        return custom_strategy(routing_intents)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


async def route_the_event(destination: Dict[str, Any], payload: Dict[str, Any]):
    # Method for routing the event to the specified destinations
    if destination["transport"].startswith("http"):
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=destination["transport"].split(".")[-1].upper(),
                url=destination["url"],
                json=payload
            )
            response.raise_for_status()
    elif destination["transport"].startswith("log"):
        log_level = getattr(logging, destination["transport"].split(".")[-1].upper())
        logger.log(log_level, f"Payload for {destination['destinationName']}: {payload}")
    else:
        raise ValueError(f"Unknown transport: {destination['transport']}")
