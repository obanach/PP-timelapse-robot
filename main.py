from Motor import Motor
from distance import HCSR04
from machine import Pin
from time import sleep
from WebServer import MicroPyServer
import network
import WebServer
import json

wlan_id = "CzopaZone"
wlan_pass = "a123456789"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print('Connecting')
while not wlan.isconnected():
    try:
        wlan.connect(wlan_id, wlan_pass)
    except OSError:
        pass
    print('.')
print("Connected... IP: " + wlan.ifconfig()[0])

distance = Pin(18, Pin.OUT)
distance.off()

led = Pin(2, Pin.OUT)
dir_pin = 22
step_pin = 21

pin_m0 = 13
pin_m1 = 12
pin_m2 = 14

step_type = 'Full'
motor = Motor(step_pin, dir_pin, pin_m0, pin_m1, pin_m2, step_type)
distance = HCSR04(18, 19)


def show_index(request):
    server.send("OK")


def MoveForward(request):
    led.on()
    server.send("HTTP/1.0 200 OK\r\n")
    data = WebServer.get_request_query_params(request)
    if distance.distance_cm() > 10:
        server.send('OK')
        motor.run(int(data['run']), True)
    else:
        server.send('OBSTACLE')
    led.off()


def MoveBackward(request):
    led.on()
    server.send("HTTP/1.0 200 OK\r\n")
    data = WebServer.get_request_query_params(request)
    if distance.distance_cm() > 10:
        server.send('OK')
        motor.run(int(data['run']), False)
    else:
        server.send('OBSTACLE')
    led.off()


def TimeLapse(request):
    led.on()
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("OK")
    data = WebServer.get_request_query_params(request)

    step_size = int(data['stepSize'])
    steps = int(data['steps'])
    delay = int(data['delay'])
    led.off()
    for step in range(steps):
        led.on()
        if distance.distance_cm() > 10:
            motor.run(step_size, True)
        else:
            print('Przeszkoda na drodze.')
        led.off()
        sleep(delay)

def Distance(request):
    server.send("HTTP/1.0 200 OK\r\n")
    data = WebServer.get_request_query_params(request)
    status = int(data['status'])
    if status == 1:
        distance.value(1)
        server.send('OK SET 1')
    else:
        distance.value(0)
        server.send('OK SET 0')


server = MicroPyServer()
server.add_route("/", show_index)
server.add_route("/forward", MoveForward)
server.add_route("/backward", MoveBackward)
server.add_route("/timelapse", TimeLapse)
server.add_route("/distance", Distance)
server.start()