from Motor import Motor
from distance import HCSR04
from machine import Pin
from time import sleep
from WebServer import MicroPyServer
import network
import WebServer
import json

wlan_id = "CzopaZone"  # Definujemy nazwę sieci WIFI
wlan_pass = "a123456789"  # Hasło dostępu do sieci wifi
wlan = network.WLAN(network.STA_IF)  # ustawiamy wifi w tyb STA_IF
wlan.active(True)  # Włączamy moduł wifi
print('Connecting')
# łączymy się z siecią
while not wlan.isconnected():
    try:
        wlan.connect(wlan_id, wlan_pass)
    except OSError:
        pass
    print('.')
print("Connected... IP: " + wlan.ifconfig()[0])

distance = Pin(18, Pin.OUT)  # ustawiamy pin wyjscia który wyświetla czy można jechać czy nie
distance.off()

led = Pin(2, Pin.OUT)  # definiujemy pin diody led
dir_pin = 22  # definiujemy pin kierunku ruchu
step_pin = 21  # definiujemy pin długości kroku

pin_m0 = 13  # definiujemy pin do kodowania rozdzielczosci ruchu
pin_m1 = 12  # definiujemy pin do kodowania rozdzielczosci ruchu
pin_m2 = 14  # definiujemy pin do kodowania rozdzielczosci ruchu

step_type = 'Full'
motor = Motor(step_pin, dir_pin, pin_m0, pin_m1, pin_m2, step_type)  # inicjujemy silnik
distance = HCSR04(18, 19)  # inicjujemy czujnik odleglosci


# strona startowa robota pokazująca ze jest wlaczony
def show_index(request):
    server.send("OK")


# ruch robota do przodu
def MoveForward(request):
    led.on()  # zapalamy diode
    server.send("HTTP/1.0 200 OK\r\n")  # wysyłamy odp do przeglądarki, że wszystko ok
    data = WebServer.get_request_query_params(request)  # odczytujemy paramtery otrzymane w zapytaniu
    if distance.distance_cm() > 10:  # sprawdzamy czy jest przeszkoda w odleglosci 10 cm
        server.send('OK')
        motor.run(int(data['run']), True)  # ruszamy do przodu o zadana ilosc
    else:
        server.send('OBSTACLE')  # wysylamy odp ze jest przeszkoda na drodze
    led.off()


# ruch robota do tylu
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


# funkcja timelapse
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


# blokowanie ruchu / wylaczanie czujnika
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


# serwer www odpowiedzialny
server = MicroPyServer()
server.add_route("/", show_index)
server.add_route("/forward", MoveForward)
server.add_route("/backward", MoveBackward)
server.add_route("/timelapse", TimeLapse)
server.add_route("/distance", Distance)
server.start()
