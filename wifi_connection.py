import network
from time import sleep
from secrets import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def scan_networks():
    networks = wlan.scan()
    print("Available networks:")
    for network_info in networks:
        print(network_info)
        
'''
0: WLAN is not enabled
1: WLAN is currently scanning for networks
2: WLAN is connecting to a network
3: WLAN is connected to a network
4: WLAN failed to connect to a network
'''
def connect_to_network(ssid, password):
    # Connect to your network
    wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    # Check if connection is successful
    if wlan.status() != 3:
        raise RuntimeError('Failed to establish a network connection')
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])


connect_to_network(WIFI_SSID, WIFI_PASSWORD)
# scan_networks()