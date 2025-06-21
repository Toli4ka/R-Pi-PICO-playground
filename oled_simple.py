# I2C Scanner MicroPython
from machine import Pin, I2C
import time
import sh1106

# You can choose any other combination of I2C pins
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

display = sh1106.SH1106_I2C(128, 64, i2c, res=None, addr=0x3c)  # 0x3c is default I2C address

display.sleep(False)   # wake up the display
display.fill(0)        # clear the display

# display.text('Privet, Adelina!', 0, 0, 1)  # text, x, y, color
# display.show()          # update the display

# # Draw a smiley face!
# center_x = 64
# center_y = 32
# radius = 30

# # Face outline
# display.ellipse(center_x, center_y, radius, radius, 1, f=False)

# # Eyes
# display.fill_rect(center_x - 10, center_y - 10, 6, 6, 1)   # Left eye
# display.fill_rect(center_x + 10, center_y - 10, 6, 6, 1)   # Right eye

# # Smile (drawn as an arc using lines)
# for x in range(-13, 14):
#     y = int(10 * ((1 - (x/13)**2)**0.5))
#     display.pixel(center_x + x, center_y + 8 + y, 1)


# Animation parameters
ball_radius = 7
x = 30
y = 30
dx = 2
dy = 2

while True:
    display.fill(0)
    # Draw the ball
    display.ellipse(x, y, ball_radius, ball_radius, 1, f=True) # type: ignore
    display.show()
    time.sleep_ms(1)

    # Update position
    x += dx
    y += dy

    # Bounce off the edges
    if x - ball_radius < 0 or x + ball_radius > 127:
        dx = -dx
    if y - ball_radius < 0 or y + ball_radius > 63:
        dy = -dy

display.show()