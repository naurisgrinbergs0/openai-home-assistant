import os
import requests
import settings as s
from utility import datetime


def request_weather(location, date, time):
    if location is None:
        location = os.getenv("LOCATION")
    if date is None:
        date = datetime.get_date()

    is_today = datetime.is_today(date)
    includes_array = []
    if time:
        includes_array.append("hours")
    if is_today:
        includes_array.append("current")

    elements_array = [
        "datetime",
        "name",
        "resolvedAddress",
        "tempmax",
        "tempmin",
        "temp",
        "humidity",
        "precip",
        "precipprob",
        "preciptype",
        "snow",
        "snowdepth",
        "windspeed",
        "windspeedmax",
        "windspeedmean",
        "windspeedmin",
        "winddir",
        "cloudcover",
        "visibility",
        "uvindex",
        "sunrise",
        "sunset",
        "moonphase",
        "description",
    ]

    path_vars = [location, date]
    params = {
        "key": os.getenv("VISUAL_CROSSING_WEATHER_KEY"),
        "unitGroup": s.locale["UNIT_SYSTEM"],
        "include": ",".join(includes_array),
        "elements": ",".join(elements_array),
    }

    try:
        result = requests.get("/".join([s.api["VISUAL_CROSSING_WEATHER_BASE_URL"]] + path_vars), params, timeout=30)
        return result.text, None

    except AttributeError:
        return None, "Location invalid"
    except Exception:
        return None, "Weather info not available"


async def get_weather(function_data):
    weather, error_text = request_weather(
        function_data.arguments.get("location"),
        function_data.arguments.get("date"),
        function_data.arguments.get("time"),
    )

    return (weather, error_text)
