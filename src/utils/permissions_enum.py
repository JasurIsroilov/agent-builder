from enum import Enum


class UserPermissions(str, Enum):

    READ_FILE = "read:file"
    UPDATE_FILE = "update:file"
    DELETE_FILE = "delete:file"
    CREATE_FILE = "create:file"

    GET_AIRCRAFT_LOCATION = "get:aircraft_location"
    GET_AIRCRAFT_FLIGHTS = "get:aircraft_flights"

    SEARCH_WEB = "search:web"
    SUMMARIZE_CONTENT = "summarize:content"
    EXTRACT_INFORMATION = "extract:information"
    ANALYZE_TOPIC = "analyze:topic"

    READ_DIPLOMA_INFORMATION = "read:diploma_information"
