from typing import Optional
from mcp.server.fastmcp import FastMCP
from models.flight_search_params import FlightSearchParams
from duffel_client import search_flights

# This file defines the MCP tool for flight search.
# It is meant to be imported and registered with the MCP server in main.py.

def register_flight_tools(mcp: FastMCP):
    @mcp.tool()
    def get_flights(
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1,
        cabin_class: str = "economy"
    ) -> dict:
        """
        MCP tool for searching available flights between two locations.
        Returns both results and debug logs.
        """
        debug_log = []
        params = FlightSearchParams(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            passengers=passengers,
            cabin_class=cabin_class
        )
        try:
            flights = search_flights(params, debug_log)
            return {
                "flights": [flight.model_dump() for flight in flights],
                "debug_log": debug_log
            }
        except Exception as e:
            return {
                "flights": [],
                "debug_log": debug_log,
                "error": str(e)
            } 