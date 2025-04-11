# Load environment variables
from dotenv import load_dotenv

# Settings and config
import settings as s
import time
from tests import test_output
import json
import threading

# Interface
from operations import realtime_event_operations
from interface.web_socket import WebSocketInterface

# models = ['gpt-4o-realtime-preview', 'gpt-4o-mini-realtime-preview']
models = ['wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview']
prompt_groups = [
    # Short prompts
    ["Izstāsti joku"],
    ["Cik pulkstenis?"],
]

latency_table = "Latency"
latency_columns = ["Model", "Prompt", "Latency"]
resource_consumption_table = "Resource consumption"
resource_consumption_columns = [
    "Model", "Prompt", "CPU start %", "CPU end %", "CPU min %", "CPU max %", "RAM start %", "RAM end %", "RAM min %",
    "RAM max %"
]


def run_tests():
    # Setup
    load_dotenv(override=True)

    request_time = 0
    ws_interface = None
    response_received_flag = threading.Event()
    first_chunk_received_flag = threading.Event()

    def on_message(message):
        if message.strip():
            data = json.loads(message)
        match data["type"]:
            case "response.audio.delta":
                if not first_chunk_received_flag.is_set():
                    latency = round((time.time() - request_time) * 1000)
                    test_output.table_append_value(latency_table, latency)
                    print(f"Latency: {latency}")
                    first_chunk_received_flag.set()
            case "response.audio.done":
                first_chunk_received_flag.clear()
                response_received_flag.set()

    # Run tests
    test_output.table_create(latency_table, latency_columns)
    for model in models:
        ws_interface = WebSocketInterface(
            model,
            realtime_event_operations.get_headers(),
            on_open_callback=realtime_event_operations.update_session,
            on_message_callback=on_message)
        ws_interface.start()
        test_output.table_append_value(latency_table, model)

        for prompt_group in prompt_groups:
            for prompt in prompt_group:
                test_output.table_append_value(latency_table, prompt)
                realtime_event_operations.insert_conversation_item(ws_interface, "user", text=prompt)
                request_time = time.time()
                realtime_event_operations.request_response(ws_interface)
                response_received_flag.wait()
                response_received_flag.clear()
                test_output.table_next_row(latency_table)

        ws_interface.stop()

    test_output.table_export(latency_table)
