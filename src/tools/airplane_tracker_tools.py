"""
Airplane tracker tool for the AirplaneTrackerAgent

These tools provide airplane information for realtime tracking of the airplanes
"""


from langchain.tools import tool
from opensky_api import OpenSkyApi

import json
import requests
from typing import TypedDict
from datetime import datetime, timezone


opensky_api = OpenSkyApi()


def get_city_details_by_coordinates(longitude: float, latitude: float):
    result = requests.get(
        url="https://api.bigdatacloud.net/data/reverse-geocode-client",
        params={
            "latitude": latitude,
            "longitude": longitude
        }
    ).json()
    return f"{result['city']} / {result['countryName']}"


@tool
def get_aircraft_location(aircraft_address: str) -> str:

    """
    Get aircraft's  current location.

    This tool performs API call to OpenSky's opensource endpoint

    Args:
        aircraft_address: icao24 of the airplane

    Returns: 
        str: Formatted city / country with the current coordinates of the airplane

    Example: 
        get_track_by_aircraft("503cb9")
    """

    try:
        track = opensky_api.get_track_by_aircraft(aircraft_address.lower())
        if not track:
            return f"Cannot get flight details of the airplane: {aircraft_address}"
        last_point = track.path[-1]
        current_location = get_city_details_by_coordinates(
            longitude=last_point.longitude,
            latitude=last_point.latitude
        )
        return (
            f"The airplane: {aircraft_address} is now in {current_location}.\n"
            f"Coordinates: longitude: {last_point.longitude}, latitude: {last_point.latitude}"
        )
    except Exception as e:
        print(str(e))
        return f"Error getting flight api"


class FlightsDict(TypedDict):
    estimated_departure_time: str
    departure_airport: str
    estimated_arrival_time: str
    airplane_call_sign: str


@tool
def parse_human_date_to_timestamp(
    input_day: int,
    input_month: int,
    input_year: int,
    input_hour: int | None,
    input_minute: int | None,
    input_second: int | None
) -> int:

    """
    Converts human inputted date into timestamp

    This tool converts human given datetime into unix timestamp.
    Hour, minute and second may not be given. (defaults to 0)

    Args:
        input_day: day number
        input_month: month number
        input_year: year number
        input_hour: given hour
        input_minute: given minute
        input_second: given second
    
    Returns:
        int: Unix timestamp

    Example:
        parse_human_date_to_timestamp(10, 12, 2026, 0, 12, 18)
    """
    return int(datetime(
        day=input_day,
        month=input_month,
        year=input_year,
        hour=input_hour or 0,
        minute=input_minute or 0,
        second=input_second or 0,
        tzinfo=timezone.utc
    ).timestamp())


@tool
def get_flights_by_aircraft(aircraft_address: str,  begin: int, end: int) -> str:

    """
    Searches for the departures for the given airplane

    This tool performs search for airplane departures for the given period of interval

    Args:
        aircraft_address: icao24 of the airplane
        begin: unix timestamp of the beginning of the interval
        end: unix timestamp of the end of the interval

    Returns:
        str: Formatted string of the departures

    Example:
        get_flights_by_aircraft("4d00da", 1791005481, 1791091881)
    """
    flights = opensky_api.get_flights_by_aircraft(
        icao24=aircraft_address.lower(),
        begin=begin,
        end=end
    )
    begin_dt = datetime.fromtimestamp(begin).strftime("%Y-%m-%d %H:%M:%S")
    end_dt = datetime.fromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")
    if not flights:
        return f"Airplane {aircraft_address} has not flights in interval {begin_dt} - {end_dt}"
    flights_data: list[FlightsDict] = []
    for flight in flights:
        flights_data.append(
            {
                "estimated_departure_time": datetime.fromtimestamp(flight.firstSeen).strftime("%Y-%m-%d %H:%M:%S"),
                "departure_airport": flight.estDepartureAirport,
                "estimated_arrival_time": datetime.fromtimestamp(flight.lastSeen).strftime("%Y-%m-%d %H:%M:%S"),
                "airplane_call_sign": flight.callsign.strip()
            }
        )
    return json.dumps(flights_data, indent=2)
