from pydantic import BaseModel

class FlightOffer(BaseModel):
    """
    Represents a single flight offer returned from the Duffel API.
    """
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    price: float
    currency: str
    stops: int 