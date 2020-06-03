import time
from pygame import Color

millis = lambda: int(round(time.time() * 1000))

def colorWipe(strip, color, wait_ms=50, inverse=False):
    """Wipe color across display a pixel at a time."""
    tab = range(strip.numPixels(), -1, -1) if inverse else range(strip.numPixels())
    for i in tab:
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
