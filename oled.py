from datetime import datetime
from tkinter.tix import Tree
import os

import adafruit_ssd1306
import board
import busio
from PIL import Image, ImageDraw, ImageFont


def updateOLED():
    """Updates the OLED with the current time"""

    i2c = busio.I2C(board.SCL, board.SDA)

    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Load a font in 2 different sizes.
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

    # Draw the text (x, y)
    while True:
        draw.text((25, 15), datetime.now().strftime("%I:%M"), font=font, fill=255)
        oled.image(image)
        oled.show()
        os.sleep(1000)


if __name__ == "__main__":
    updateOLED()
