import esp
esp.osdebug(None)

import network
import nat_router
from time import sleep

# 1. Connect to external Wi-Fi (Station mode)
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SSID", "PASSWORD") # change to your WiFi's SSID & PWD

print('Connecting to Wi-Fi...', end='')
while not sta.isconnected():
    print('.', end='')
    sleep(1)
print('\nConnected to external Wi-Fi with IP:', sta.ifconfig()[0])

# 2. Set up local Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Mata4Kaki5', password='GuaMusang', authmode=3) # change to your AP's SSID & PWD
# Set AP IP and gateway
ap_ip = '10.10.6.1'
ap.ifconfig((ap_ip, '255.255.255.0', ap_ip, ap_ip))
print("AP mode active with IP:", ap.ifconfig()[0])

# 3. Initialize and start the NAT Router
print('Starting NAT Router...')
nat = nat_router.NATRouter()
nat.init(ap, sta)
nat.start()

print('AP Config:', ap.ifconfig())
print('STA Config:', sta.ifconfig())

# Example: Adding a port mapping (uncomment to use)
# Forward port 8080 of the ESP32 to port 80 of a device at 10.10.6.2
# nat.add_portmap(nat_router.PROTO_TCP, sta.ifconfig()[0], 8080, '10.10.6.2', 80)

print('NAT Router is active.')

