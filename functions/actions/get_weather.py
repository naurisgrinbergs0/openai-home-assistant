import settings as s
import os
from utility import datetime
import requests
from response import response
from telegram_api import messaging, recipients

# TODO: refactor file


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
        result = requests.get(
            "/".join([s.api["VISUAL_CROSSING_WEATHER_BASE_URL"]] + path_vars), params
        )
        return result.text, None
    except AttributeError as e:
        return None, "{location invalid}"
    except Exception as e:
        return None, "{weather info not available}"


async def get_weather(called_function, prompt):
    weather, error_text = request_weather(
        called_function.arguments.get("location"),
        called_function.arguments.get("date"),
        called_function.arguments.get("time"),
    )

    prompt = ""
    if weather:
        prompt = prompt + f"|Weather: {weather}"
    elif error_text:
        prompt = f"{error_text}"

    post_action = called_function.arguments.get("post_action_send_telegram_message")
    if post_action:
        users = recipients.find_recipients(
            chat_ids=recipients.parse_recipient_array(post_action.get("recipients"))
        )
        await messaging.send_message(users, weather)
    else:
        response.respond_in_realtime_async(
            prompt,
            # tool_call_id_replying_to=called_function.call_id, # TODO : implement so that message can respond to  tool call
        )
