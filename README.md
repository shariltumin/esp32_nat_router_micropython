# ESP32 NAT Router for MicroPython

This project implements a NAT (Network Address Port Translation) router on the ESP32 using MicroPython. It allows the ESP32 to act as a bridge between an external Wi-Fi network (STA mode) and a local network (AP mode), enabling devices connected to the ESP32's Access Point to access the internet through the ESP32's station connection.

## File Structure

```
.
├── boards
│   └── ESP32_AP_NAT
│       ├── board.json
│       ├── board.md
│       ├── manifest.py
│       ├── mpconfigboard.cmake
│       ├── mpconfigboard.h
│       └── sdkconfig.kaki5
├── build-ESP32_AP_NAT
│   ├── firmware.bin
│   └── sdkconfig
├── esp32_common.cmake-NAT
├── log
│   ├── start_nat.txt
│   └── sysinfo.txt
├── mpb_esp32_ap_nat.sh
├── mpconfigport.h-AP-NAT
├── MPY
│   └── sysinfo.mpy
├── README.md
├── start_nat.py
├── USER_MANUAL.md
└── xmod
    └── nat_router.c
```

## Features

- **NAPT Support:** Enables multiple devices on the local AP to share a single external IP address.
- **Port Mapping:** Supports static port forwarding for TCP and UDP, allowing external access to services hosted on devices within the local network.
- **Configurable DNS:** Automatically uses DNS from the station interface or allows for a custom fallback DNS.
- **MicroPython Integration:** Easy-to-use Python API for initializing, starting, and managing the NAT router.

## Installation

To use this module, you need to include `nat_router.c` in your MicroPython build as a user module.

1. Copy `nat_router.c` to your MicroPython user modules directory.
2. Recompile MicroPython for ESP32 with the user module enabled.
3. Flash the resulting firmware to your ESP32.

## Quick Start

```python
import network
import nat_router
from time import sleep

# 1. Connect to external Wi-Fi (Station mode)
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("YOUR_SSID", "YOUR_PASSWORD")
while not sta.isconnected():
    sleep(1)
print('Connected to external Wi-Fi:', sta.ifconfig()[0])

# 2. Set up local Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32_Router', password='password123', authmode=3)
ap.ifconfig(('10.10.6.1', '255.255.255.0', '10.10.6.1', '10.10.6.1'))
print("AP mode active with IP:", ap.ifconfig()[0])

# 3. Initialize and start the NAT Router
nat = nat_router.NATRouter()
nat.init(ap, sta)
nat.start()

print('NAT Router is running!')
```

## Port Mapping Example

```python
# Forward external port 8080 to internal IP 10.10.6.2 on port 80 (TCP)
nat.add_portmap(nat_router.PROTO_TCP, '192.168.1.100', 8080, '10.10.6.2', 80)
```

## License

This project is open-source and available under the MIT License.
