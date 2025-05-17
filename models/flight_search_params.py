from typing import Optional
from pydantic import BaseModel

class FlightSearchParams(BaseModel):
    """
    Represents the parameters required to search for flights.
    """
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    passengers: int = 1
    cabin_class: str = "economy" 