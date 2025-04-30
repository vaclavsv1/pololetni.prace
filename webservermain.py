import network
import time

ssid = "fcvp"     # <-- Změň na svůj název Wi-Fi
password = "12345678"  # <-- Změň na své heslo

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Připojuji se k Wi-Fi...")
    wlan.connect(ssid, password)

    timeout = 10  # čekej max. 10 sekund
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

if wlan.isconnected():
    print("\n✅ Připojeno! IP adresa:", wlan.ifconfig()[0])
else:
    print("\n❌ Nepodařilo se připojit.")