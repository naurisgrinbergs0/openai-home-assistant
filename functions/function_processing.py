import json
import actions.send_telegram_picture
import actions.take_picture
import actions.toggle_lights
import settings as s
import asyncio
import actions


def process_function_calls(func_calls):
    callable_functions = []

    def Object(**kwargs):
        return type("Object", (), kwargs)

    # Object = lambda **kwargs: type("Object", (), kwargs)

    for func in func_calls:
        args = None
        if func["arguments"] != "":
            args = json.loads(func["arguments"][2:] if func["arguments"][:2] == "{}" else func["arguments"])
        callable_function = Object(
            call_id=func["id"],
            name=func["name"],
            arguments=(args),
        )
        callable_functions.append(callable_function)

    async def call_functions():
        for called_function in callable_functions:
            print(f"|-- Executing function [{called_function.name}]")
            await call_function(called_function)

    asyncio.run(call_functions())


async def call_function(called_function):
    match (called_function.name):
        case s.functions["GET_WEATHER"]:
            return await actions.get_weather(called_function)
        case s.functions["TAKE_PICTURE"]:
            return await actions.take_picture(called_function)
        case s.functions["TOGGLE_LIGHTS"]:
            return await actions.toggle_lights(called_function)
        case s.functions["TELEGRAM_SEND_MESSAGE"]:
            return await actions.send_telegram_message(called_function)
        case s.functions["TELEGRAM_SEND_PICTURE"]:
            return await actions.send_telegram_picture(called_function)
        case s.functions["GET_USER_INPUT"]:
            return await actions.get_user_input(called_function)
