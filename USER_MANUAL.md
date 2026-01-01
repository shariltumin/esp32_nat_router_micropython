# ESP32 NAT Router User Manual

This manual provides detailed instructions on how to use the `nat_router` module in MicroPython.

## Table of Contents

1. [Introduction](#introduction)
2. [API Reference](#api-reference)
3. [Configuration](#configuration)
4. [Port Mapping Guide](#port-mapping-guide)
5. [Troubleshooting](#troubleshooting)

## Introduction

The `nat_router` module leverages the ESP-IDF's NAPT capabilities to provide a functional NAT router. It manages the DHCP server, DNS settings, and IP forwarding rules necessary to bridge two network interfaces.

## API Reference

### Module Constants

- `nat_router.PROTO_TCP`: Constant for the TCP protocol (6).
- `nat_router.PROTO_UDP`: Constant for the UDP protocol (17).
- `nat_router.PROTO_ICMP`: Constant for the ICMP protocol (1).

### Class: `NATRouter`

#### `init(ap_if, sta_if)`
Initializes the router with the Access Point and Station interfaces.
- `ap_if`: The `network.WLAN(network.AP_IF)` object.
- `sta_if`: The `network.WLAN(network.STA_IF)` object.

#### `start(dns=None)`
Starts the NAT router.
- `dns` (optional): A string containing the IP address of a custom DNS server. If not provided, the router will try to use the DNS server provided by the station interface, falling back to `8.8.8.8`.

#### `stop()`
Disables NAPT and restarts the DHCP server on the AP interface without NAPT options.

#### `add_portmap(proto, maddr, mport, daddr, dport)`
Adds a static port mapping.
- `proto`: The protocol (`PROTO_TCP` or `PROTO_UDP`).
- `maddr`: The "master" IP address (usually the IP of the ESP32's station interface).
- `mport`: The port on the master interface to listen on.
- `daddr`: The destination IP address (the device on the local network).
- `dport`: The destination port on the local device.
- **Returns:** `True` if successful, `False` otherwise.

#### `remove_portmap(proto, mport)`
Removes a port mapping.
- `proto`: The protocol of the mapping to remove.
- `mport`: The master port of the mapping to remove.
- **Returns:** `True` if successful, `False` otherwise.

## Configuration

### Basic Setup

The most common setup involves connecting the ESP32 to an existing Wi-Fi network and then starting the AP.

```python
import network
import nat_router

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SSID", "PASSWORD")

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.ifconfig(('10.10.6.1', '255.255.255.0', '10.10.6.1', '10.10.6.1'))

nat = nat_router.NATRouter()
nat.init(ap, sta)
nat.start()
```

### Using Custom DNS

If you want to force all connected devices to use a specific DNS server (e.g., Cloudflare):

```python
nat.start(dns="1.1.1.1")
```

## Port Mapping Guide

Port mapping (or port forwarding) allows devices on the internet (or the external network) to access services on devices connected to your ESP32's AP.

### Example: Web Server

If you have a web server running on a device with IP `10.10.6.2` on port `80`, and your ESP32 has an external IP of `192.168.1.100`, you can forward port `8080` of the ESP32 to the web server:

```python
nat.add_portmap(nat_router.PROTO_TCP, '192.168.1.100', 8080, '10.10.6.2', 80)
```

Now, anyone on the `192.168.1.x` network can access the web server by navigating to `http://192.168.1.100:8080`.

## Troubleshooting

- **No Internet access on clients:** Ensure the Station interface is connected and has a valid IP and gateway.
- **DNS issues:** If websites don't load but IPs work, check your DNS settings. Try setting a custom DNS in `nat.start(dns="8.8.8.8")`.
- **Port mapping fails:** Ensure the protocol and ports are correct. The master IP should be the IP assigned to the ESP32's station interface.
- **Interface names:** The module uses "WIFI_STA_DEF" and "WIFI_AP_DEF". These are standard for ESP-IDF, but ensure your MicroPython build hasn't changed them.
- **Type Opacity Problem:** We need a `typedef` in the module:
```C
// Define the wlan_if_obj_t structure (needed for MicroPython internal use)
typedef struct _wlan_if_obj_t {
    mp_obj_base_t base;
    esp_netif_t *netif;
} wlan_if_obj_t;
```
MicroPython's WLAN interface object (`wlan_if_obj_t`) is defined internally in MicroPython's `network_wlan.c` network module implementation, but it's not exposed in public headers. We need the `esp_netif_t *netif` since the module receives WLAN objects as parameters. This creates tight coupling to MicroPython's internal implementation (could break if the structure changes)

