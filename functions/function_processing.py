import json
import asyncio
from functions.actions import get_weather, take_picture, toggle_lights, send_telegram_message, send_telegram_picture, get_user_input
import settings as s


def process_function_calls(func_calls):
    callable_functions = []
    call_results = []

    def Object(**kwargs):
        return type("Object", (), kwargs)

    for func in func_calls:
        args = None
        if func["arguments"] != "":
            args = json.loads(func["arguments"][2:] if func["arguments"][:2] == "{}" else func["arguments"])
        callable_function = Object(
            call_id=func["call_id"],
            name=func["name"],
            arguments=(args),
        )
        callable_functions.append(callable_function)

    async def call_functions():
        tasks = [call_function(func) for func in callable_functions]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for func, (result, error) in zip(callable_functions, results):
            call_results.append({"result": result, "error": error, "call_id": func.call_id})

    asyncio.run(call_functions())

    return call_results


async def call_function(called_function):
    if called_function.name == s.functions["GET_WEATHER"]:
        return await get_weather.get_weather(called_function)
    if called_function.name == s.functions["TAKE_PICTURE"]:
        return await take_picture.take_picture(called_function)
    if called_function.name == s.functions["TOGGLE_LIGHTS"]:
        return await toggle_lights.toggle_lights(called_function)
    if called_function.name == s.functions["TELEGRAM_SEND_MESSAGE"]:
        return await send_telegram_message.telegram_send_message(called_function)
    if called_function.name == s.functions["TELEGRAM_SEND_PICTURE"]:
        return await send_telegram_picture.send_telegram_picture(called_function)
    if called_function.name == s.functions["GET_USER_INPUT"]:
        return await actions.get_user_input(called_function)
