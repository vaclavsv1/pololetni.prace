import network

def pripoj_wifi(ssid, heslo):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Připojuji se k síti...')
        wlan.connect(ssid, heslo)
        while not wlan.isconnected():
            pass
    print('Připojeno, IP adresa:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]
