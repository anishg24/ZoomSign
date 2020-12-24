# API PART
import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

JSON_URL = "http://192.168.1.126:5000/updates"


# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)


requests.set_socket(socket, esp)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected!")
print()



# DISPLAY PART
import adafruit_display_text.label
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix)

def scroll(line):
        line.x = line.x - 1
        line_width = line.bounding_box[2]
        if line.x < -line_width:
            line.x = display.width

# Create two lines of text to scroll. Besides changing the text, you can also
# customize the color and font (using Adafruit_CircuitPython_Bitmap_Font).
# To keep this demo simple, we just used the built-in font.
# The Y coordinates of the two lines were chosen so that they looked good
# but if you change the font you might find that other values work better.
while True:
    try:
        r = requests.get(JSON_URL)
        print("Fetched json from", JSON_URL)
        message=r.json()["message"]
        status=r.json()["status"]
        freetime=r.json()["in_free_time"]
        r.close()
    except:
        continue

    if freetime:
        message="FREE!"
        top_txt="Anish is"
    else:
        top_txt="Anish in"
    colors = [0xff0000, 0xffff00, 0x00ff00]
    #
    line1 = adafruit_display_text.label.Label(
        terminalio.FONT,
        color=colors[status],
        text=top_txt)
    line1.x = 8
    line1.y = 8

    line2 = adafruit_display_text.label.Label(
        terminalio.FONT,
        color=0x0080ff,
        text=message)
    line2.x = display.width
    line2.y = 24
    # Put each line of text into a Group, then show that group.
    g = displayio.Group()
    g.append(line1)
    g.append(line2)
    display.show(g)

    for _ in range(len(line2.text)*20):
        scroll(line2)
        time.sleep(0.1)
        display.refresh(minimum_frames_per_second=0)