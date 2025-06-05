import network
import socket
import time
import dht
import machine

ssid = "fcvp"
password = "12345678"

# Wi-Fi připojení
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Připojuji se k Wi-Fi...", end="")
    wlan.connect(ssid, password)

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

if wlan.isconnected():
    print("\n✅ Připojeno! IP:", wlan.ifconfig()[0])
else:
    print("\n❌ Nepodařilo se připojit k Wi-Fi.")
    # Pokud Wi-Fi není, dál neběžíme
    raise SystemExit

ip = wlan.ifconfig()[0]

# Senzory
sensor_dht = dht.DHT11(machine.Pin(16))
soil = machine.ADC(26)

def read_sensors():
    try:
        sensor_dht.measure()
        temp = sensor_dht.temperature()
        hum = sensor_dht.humidity()
    except Exception as e:
        print("Chyba DHT:", e)
        temp = "chyba"
        hum = "chyba"
    soil_val = soil.read_u16()
    return temp, hum, soil_val

def load_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        print("Chyba čtení souboru", filename, ":", e)
        return None

def web_response(path):
    if path == "/" or path == "/index.html":
        html = load_file("index.html")
        if html is None:
            return "HTTP/1.0 500 Internal Server Error\r\n\r\nSoubor index.html nenalezen"
        temp, hum, soil_val = read_sensors()
        html = html.replace("{{temp}}", str(temp))
        html = html.replace("{{hum}}", str(hum))
        html = html.replace("{{soil}}", str(soil_val))
        header = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        return header + html

    elif path == "/style.css":
        css = load_file("style.css")
        if css is None:
            return "HTTP/1.0 404 Not Found\r\n\r\n"
        header = "HTTP/1.0 200 OK\r\nContent-Type: text/css\r\n\r\n"
        return header + css

    else:
        return "HTTP/1.0 404 Not Found\r\n\r\n"

# Start webserveru
addr = socket.getaddrinfo(ip, 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("🌐 Webserver běží na http://" + ip)

while True:
    try:
        cl, addr = s.accept()
        print("Klient:", addr)
        req = cl.recv(1024).decode("utf-8")
        print("Request:", req.split("\n")[0])

        # Získáme cestu požadavku
        first_line = req.split("\n")[0]
        path = first_line.split(" ")[1] if len(first_line.split(" ")) > 1 else "/"

        response = web_response(path)
        cl.send(response.encode())
        cl.close()

    except Exception as e:
        print("Chyba serveru:", e)
        cl.close()
