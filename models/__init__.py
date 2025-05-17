# Mrks models/ as a Python package, allowing you to import with from models import FlightSearchParams, FlightOffer.

from .flight_search_params import FlightSearchParams
from .flight_offer import FlightOffer

__all__ = ["FlightSearchParams", "FlightOffer"] 