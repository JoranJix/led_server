from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from rpi_ws281x import PixelStrip, Color

# LED-Konfiguration
LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

# LEDs initialisieren
strip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)
strip.begin()

class LEDControlRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, message):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': message}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        if self.path == '/set_led':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = json.loads(post_data)
            
            led_index = post_data.get('led', 0)
            color = post_data.get('color', {'r': 0, 'g': 0, 'b': 0})

            r = color.get('r', 0)
            g = color.get('g', 0)
            b = color.get('b', 0)
            strip.setPixelColor(led_index, Color(r, g, b))
            strip.show()

            self._send_response(200, f'LED {led_index} wurde aktualisiert')
        else:
            self._send_response(404, 'Not Found')

def run_server():
    PORT = 8000
    server = HTTPServer(("", PORT), LEDControlRequestHandler)
    print(f"Server läuft auf Port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
