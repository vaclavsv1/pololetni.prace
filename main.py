import dht
from machine import Pin
import time

# Nastavení pinu pro DHT11 (používáme GP16)
sensor = dht.DHT11(Pin(16))  # Používáme GPIO16 (pin 21 na Pico)

while True:
    try:
        # Měření teploty a vlhkosti
        sensor.measure()
        teplota = sensor.temperature()
        vlhkost = sensor.humidity()

        # Výpis hodnot do konzole
        print('Teplota: {} °C'.format(teplota))
        print('Vlhkost: {} %'.format(vlhkost))

    except OSError as e:
        print('Chyba při čtení dat ze senzoru')

    # Čekání 2 sekundy před dalším měřením
    time.sleep(2)