import network
import socket
from time import sleep
from machine import Pin, I2C
from secrets import WIFI_SSID, WIFI_PASSWORD
import sh1106

led = Pin('LED', Pin.OUT)

def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to your network
    wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        sleep(1)

    # Check if connection is successful
    if wlan.status() != 3:
        print('Failed to establish a network connection')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def init_display():
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, res=None, addr=0x3c, rotate=180)
    display.sleep(False)
    display.fill(0)
    return display

# HTML template for the webpage
def webpage(message, state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>Led Control</h2>
            <form action="./lighton">
                <input type="submit" value="Light on" />
            </form>
            <br>
            <form action="./lightoff">
                <input type="submit" value="Light off" />
            </form>
            <p>LED state: {state}</p>
            <h2>OLED Message</h2>
            <form action="/display" method="get">
                <input type="text" name="msg" value="{message}" />
                <input type="submit" value="Display on OLED" />
            </form>
        </body>
        </html>
        """
    return str(html)

init_wifi(WIFI_SSID, WIFI_PASSWORD)
oled = init_display()

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print('Listening on', addr)

# Initialize variables
state = "OFF"
oled_message = ""

# Main loop to listen for connections
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:
            request = request.split()[1]
            print('Request:', request)
        except IndexError:
            pass
        
        # Process the request and update variables
        if request == '/lighton?':
            print("LED on")
            led.value(1)
            state = "ON"
        elif request == '/lightoff?':
            led.value(0)
            state = 'OFF'
        # OLED display
        elif request.startswith('/display'):
            # Parse the message from the URL
            import ure
            match = ure.search(r"msg=([^& ]+)", request)
            if match:
                oled_message = match.group(1).replace('+', ' ')
                # Display on OLED
                oled.fill(0)
                oled.text(oled_message, 0, 0)
                oled.show()

        # Generate HTML response
        response = webpage(oled_message, state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')