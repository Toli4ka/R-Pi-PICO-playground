import network
from time import sleep
import urequests
from machine import Pin, I2C
import sh1106
from secrets import WIFI_SSID, WIFI_PASSWORD, WEATHER_API_KEY

CITY = "Munich"

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
        return True

def init_display():
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, res=None, addr=0x3c, rotate=180)
    display.sleep(False)
    display.fill(0)
    return display

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    response = urequests.get(url)
    data = response.json()
    response.close()  # Close the response to free up resources
    if data.get("main") and data.get("weather"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        if desc == "Clouds":
            desc = "Cloudy"
        elif desc == "Clear":
            desc = "Sunny"
        elif desc == "Rain":
            desc = "Rainy"
        elif desc == "Snow":
            desc = "Snowy"
        else:
            desc = "Weather not recognized"
        return f"{CITY}\nTemp: {int(temp)}C\n{desc}\nHum: {humidity}%"
    else:
        return "No data"

if init_wifi(WIFI_SSID, WIFI_PASSWORD):
    # Initialize the display
    display = init_display()
    try:
        weather = get_weather()
        display.text_multiline(weather, 0, 0, 1)
        display.show()

    except Exception as e:
        # Handle any exceptions during the request
        print('Error during request:', e)
        display.text('Error!', 0, 0)
        display.show()
    