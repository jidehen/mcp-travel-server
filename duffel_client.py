import json
import httpx
from typing import List
from models import FlightSearchParams, FlightOffer
from config.duffel_config import DUFFEL_API_URL, DUFFEL_API_KEY


def search_flights(params: FlightSearchParams, debug_log: list) -> List[FlightOffer]:
    """
    Searches for flights using the Duffel API.
    This function builds the request, sends it to Duffel, logs every step, and parses the response.
    Args:
        params: FlightSearchParams object with user search criteria
        debug_log: List to collect debug messages for client-side troubleshooting
    Returns:
        List of FlightOffer objects representing available flights
    Raises:
        Exception with error details if the search fails
    """
    debug_log.append(f"Starting search with params: {params}")
    try:
        slices = [
            {
                "origin": params.origin,
                "destination": params.destination,
                "departure_date": params.departure_date
            }
        ]
        debug_log.append(f"Initial slices: {json.dumps(slices)}")
        if params.return_date:
            slices.append({
                "origin": params.destination,
                "destination": params.origin,
                "departure_date": params.return_date
            })
            debug_log.append(f"Added return slice: {json.dumps(slices[-1])}")
        passengers = [{"type": "adult"}] * params.passengers
        debug_log.append(f"Passengers: {json.dumps(passengers)}")
        debug_log.append(f"Cabin class: {params.cabin_class}")
        request_data = {
            "data": {
                "slices": slices,
                "passengers": passengers,
                "cabin_class": params.cabin_class
            }
        }
        debug_log.append(f"Request data: {json.dumps(request_data)}")
        headers = {
            "Authorization": f"Bearer {DUFFEL_API_KEY}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }
        params_query = {
            "return_offers": "true",
            "supplier_timeout": 30000
        }
        debug_log.append(f"Headers: {headers}")
        debug_log.append(f"Query params: {params_query}")
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                DUFFEL_API_URL,
                headers=headers,
                params=params_query,
                json=request_data
            )
            debug_log.append(f"Duffel API status: {response.status_code}")
            debug_log.append(f"Duffel API response: {response.text}")
            response.raise_for_status()
            data = response.json()["data"]
        offers = data.get("offers", [])
        debug_log.append(f"Offers found: {len(offers)}")
        flight_offers = []
        for offer in offers:
            for slice in offer["slices"]:
                segment = slice["segments"][0]
                flight_offers.append(FlightOffer(
                    airline=segment["operating_carrier"]["name"],
                    flight_number=segment["operating_carrier_flight_number"],
                    departure_time=segment["departing_at"],
                    arrival_time=segment["arriving_at"],
                    price=float(offer["total_amount"]),
                    currency=offer["total_currency"],
                    stops=len(slice["segments"]) - 1
                ))
        debug_log.append(f"Returning {len(flight_offers)} flight offers")
        return flight_offers
    except Exception as e:
        debug_log.append(f"Exception: {str(e)}")
        raise Exception(f"Error searching flights: {str(e)}") 