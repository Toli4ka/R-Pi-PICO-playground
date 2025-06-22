# I2C Scanner MicroPython
from machine import Pin, I2C
import time
import sh1106 
import math
# Initialize I2C for the OLED display
# You can choose any other combination of I2C pins
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

display = sh1106.SH1106_I2C(128, 64, i2c, res=None, addr=0x3c, rotate=180)  # 0x3c is default I2C address

display.sleep(False)   # wake up the display
display.fill(0)        # clear the display

# # Display a welcome message
# display.text('Privet, Adelina!', 0, 0, 1)  # text, x, y, color
# display.show()          # update the display

# Draw a smiley face!
def draw_smiley_face():
    # Center coordinates and radius for the face
    center_x = 64
    center_y = 32
    radius = 30

    # Face outline
    display.ellipse(center_x, center_y, radius, radius, 1, f=False) # type: ignore

    # Eyes
    display.fill_rect(center_x - 10, center_y - 10, 6, 6, 1)   # Left eye
    display.fill_rect(center_x + 10, center_y - 10, 6, 6, 1)   # Right eye

    # Smile (drawn as an arc using lines)
    for x in range(-13, 14):
        y = int(10 * ((1 - (x/13)**2)**0.5))
        display.pixel(center_x + x, center_y + 8 + y, 1)

    display.show()


def animate_ball():
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


def draw_sun(display, x, y):
    display.ellipse(x+7, y+7, 4, 4, 1, f=False)

    # Rays (4 sides)
    display.fill_rect(x+6, y, 3, 2, 1)        # Top
    display.fill_rect(x+6, y+13, 3, 2, 1)     # Bottom
    display.fill_rect(x, y+6, 2, 3, 1)        # Left
    display.fill_rect(x+13, y+6, 2, 3, 1)     # Right

    # Diagonal rays (corners)
    display.fill_rect(x+1, y+1, 2, 2, 1)      # Top-left
    display.fill_rect(x+12, y+1, 2, 2, 1)     # Top-right
    display.fill_rect(x+1, y+12, 2, 2, 1)     # Bottom-left
    display.fill_rect(x+12, y+12, 2, 2, 1)    # Bottom-right


def draw_cloud(display, x, y):
    # Outline
    # Bottom
    y = y - 3
    display.hline(x+2, y+13, 12, 1)
    display.pixel(x+1, y+12, 1)
    display.pixel(x+14, y+12, 1)
    display.pixel(x+15, y+11, 1)

    # Lower left puff
    display.pixel(x+1, y+11, 1)
    display.pixel(x+1, y+10, 1)
    display.pixel(x+2, y+9, 1)
    display.hline(x+3, y+8, 2, 1)
    display.pixel(x+4, y+7, 1)

    # Left-middle puff
    display.hline(x+5, y+6, 3, 1)
    display.pixel(x+4, y+7, 1)
    display.pixel(x+8, y+6, 1)

    # Top bump
    display.hline(x+8, y+5, 4, 1)
    display.pixel(x+7, y+6, 1)
    display.pixel(x+12, y+6, 1)

    # Right bump
    display.hline(x+12, y+7, 3, 1)
    display.pixel(x+15, y+8, 1)
    display.pixel(x+15, y+9, 1)
    display.pixel(x+15, y+10, 1)
    display.pixel(x+15, y+11, 1)


def draw_rain(display, x, y):
    draw_cloud(display, x, y-2)
    # Draw raindrops
    for i in range(3):
        display.line(x+4+4*i, y+11, x+2+4*i, y+13, 1)

def draw_snowflake(display, x, y):
    # This draws an 8x8 snowflake, with center at (x+4, y+4)
    # Center "hole"
    display.pixel(x+4, y+4, 0)
    # Main arms (up, down, left, right, 2 pixels each)
    display.pixel(x+4, y+2, 1)
    display.pixel(x+4, y+1, 1)
    display.pixel(x+4, y+6, 1)
    display.pixel(x+4, y+7, 1)
    display.pixel(x+2, y+4, 1)
    display.pixel(x+1, y+4, 1)
    display.pixel(x+6, y+4, 1)
    display.pixel(x+7, y+4, 1)
    # Diagonal arms (make a 6-armed snowflake)
    display.pixel(x+2, y+2, 1)
    display.pixel(x+1, y+1, 1)
    display.pixel(x+6, y+6, 1)
    display.pixel(x+7, y+7, 1)
    display.pixel(x+6, y+2, 1)
    display.pixel(x+7, y+1, 1)
    display.pixel(x+2, y+6, 1)
    display.pixel(x+1, y+7, 1)

    # Tips (make them a bit thicker for a stylized look)
    # Vertical
    display.pixel(x+8, y+3, 1)
    display.pixel(x+8, y+12, 1)
    # Horizontal
    display.pixel(x+3, y+8, 1)
    display.pixel(x+12, y+8, 1)
    # Diagonal /
    display.pixel(x+3, y+3, 1)
    display.pixel(x+13, y+13, 1)
    # Diagonal \
    display.pixel(x+13, y+3, 1)
    display.pixel(x+3, y+13, 1)

display.fill(0)
draw_sun(display, 0, 0)
draw_cloud(display, 20, 0)
draw_rain(display, 40, 0)
draw_snowflake(display, 60, 30)
display.show()