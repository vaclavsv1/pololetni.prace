import dht
from machine import Pin
import time

# Používáme GPIO16 (fyzický pin 21) pro datový pin senzoru
sensor = dht.DHT11(Pin(16))

while True:
    try:
        sensor.measure()  # Spustí měření
        teplota = sensor.temperature()
        vlhkost = sensor.humidity()
        print("Teplota: {} °C".format(teplota))
        print("Vlhkost: {} %".format(vlhkost))
    except OSError as e:
        print("Chyba při čtení dat ze senzoru:", e)

    time.sleep(2)