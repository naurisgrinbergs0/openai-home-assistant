import threading
import websocket


class WebSocketInterface:

    def __init__(
            self,
            url,
            header,
            on_open_callback=None,
            on_close_callback=None,
            on_error_callback=None,
            on_message_callback=None):

        self.url = url
        self.header = header
        self.ws_app = None
        self.connected_or_failed = threading.Event()

        self.on_open_callback = on_open_callback
        self.on_close_callback = on_close_callback
        self.on_error_callback = on_error_callback
        self.on_message_callback = on_message_callback

    def _on_open(self, _):
        print("|-- WebSocket connected")
        self.connected_or_failed.set()
        if self.on_open_callback:
            self.on_open_callback(self)

    def _on_close(self, _, close_status_code, close_msg):
        print("|-- WebSocket disconnected:", close_status_code, close_msg)
        self.connected_or_failed.set()
        if self.on_close_callback:
            self.on_close_callback(close_status_code, close_msg)

    def _on_message(self, _, message):
        if self.on_message_callback:
            self.on_message_callback(message)

    def _on_error(self, _, error):
        print("|-- WebSocket error:", error)
        if self.on_error_callback:
            self.on_error_callback(error)

    def start(self):
        self.connected_or_failed.clear()
        self.ws_app = websocket.WebSocketApp(
            self.url,
            header=self.header,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close)

        def serve_websocket_loop():
            self.ws_app.run_forever()

        ws_thread = threading.Thread(target=serve_websocket_loop, args=())
        ws_thread.daemon = True
        ws_thread.start()

        self.connected_or_failed.wait()

    def stop(self):
        self.connected_or_failed.clear()
        if self.ws_app:
            self.ws_app.close()
            self.ws_app = None

    def send_message(self, data):
        if not self.ws_app:
            self.start()

        self.ws_app.send(data)
