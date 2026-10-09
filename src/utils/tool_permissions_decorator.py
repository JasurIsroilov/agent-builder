from functools import wraps


# This is the simulation variable and should be removed for production use
USER_PERMISSIONS: list[str] = [
    #"read:file",
    #"update:file",
    #"delete:file",
    #"create:file",
    #"get:aircraft_location",
    "get:aircraft_flights",
    "search:web",
    "summarize:content",
    "extract:information",
    "analyze:topic",
    "read:diploma_information",
]


def tool_permission(required_permission: str):

    """
    A custom decorator to check user permissions before executing a tool.
    This is the basic decorator which simulates the security compliance
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, ** kwargs):
            if required_permission not in USER_PERMISSIONS:
                return "User cannot access this functionality of the AI agent."
            return func(*args, **kwargs)
        return wrapper
    return decorator
