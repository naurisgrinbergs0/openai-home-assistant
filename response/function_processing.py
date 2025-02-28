import functions.take_picture as take_picture
import functions.toggle_lights as toggle_lights
import functions.get_weather as get_weather
import functions.generate_image as generate_image
import json
import settings as s
import asyncio
import threading


def process_function_calls(func_calls, prompt):
    called_functions = []

    # TODO: ask assistant 'say hello and give me temperature of today' to check if it is possible to receive tool call and text response at the same time

    # messages.append({"role": "assistant", "content": tool_calls})

    for func in func_calls:
        Object = lambda **kwargs: type("Object", (), kwargs)
        args = None
        if func["arguments"] != "":
            args = json.loads(
                func["arguments"][2:]
                if func["arguments"][:2] == "{}"
                else func["arguments"]
            )
        called_function = Object(
            call_id=func["id"],
            name=func["name"],
            arguments=(args),
        )
        called_functions.append(called_function)

    async def call_functions():
        for called_function in called_functions:
            print(f"|-- Executing function [{called_function.name}]")
            await call_function(called_function, prompt)

    asyncio.run(call_functions())


async def call_function(called_function, prompt):
    if called_function.name == s.functions["TAKE_PICTURE"]:
        take_picture.take_picture(called_function, prompt)
    elif called_function.name == s.functions["GET_WEATHER"]:
        await get_weather.get_weather(called_function, prompt)
    elif called_function.name == s.functions["TOGGLE_LIGHTS"]:
        toggle_lights.toggle_lights()
    elif called_function.name == s.functions["GENERATE_IMAGE"]:
        await generate_image.generate_image(called_function)
