# led_server

Creates a little server on a raspberry pi to drive single LEDs in WS2812B LED Strips via html-POST

to test it send follwing command

curl -X POST -H "Content-Type: application/json" -d '{"led": 3, "color": {"r": 255, "g": 0, "b": 0}}' http://localhost:8000/set_led
