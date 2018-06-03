from PIL import Image, ImageDraw

"""Debug values for print in an image sc2 areas
:param area: the array of tuples with positions
:param filename: the filename for the png value. By default is test. Don't need extension
"""


def print_area(area, filename="test"):
    image = Image.new("RGB", (200, 200), 0xffffff)
    draw = ImageDraw.Draw(image)
    for xy in area:
        draw.point(xy, 0xff00ff)
    image.save(f"{filename}.jpg", format='JPEG')
