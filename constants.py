# LED strip configuration:
LED_COUNT      = 15      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


NOTES = {
    65.41:'C2',
    69.30:'C2#',
    73.42:'D2',
    77.78:'E2b',
    82.41:'E2',
    87.31:'F2',
    92.50:'F2#',
    98.00:'G2',
    103.80:'G2#',
    110.00:'A2',
    116.50:'B2b',
    123.50:'B2',
    130.80:'C3',
    138.60:'C3#',
    146.80:'D3',
    155.60:'E3b',
    164.80:'E3',
    174.60:'F3',
    185.00:'F3#',
    196.00:'G3',
    207.70:'G3#',
    220.00:'A3',
    233.10:'B3b',
    246.90:'B3',
    261.60:'C4',
    277.20:'C4#',
    293.70:'D4',
    311.10:'E4b',
    329.60:'E4',
    349.20:'F4',
    370.00:'F4#',
    392.00:'G4',
    415.30:'G4#',
    440.00:'A4',
    466.20:'B4b',
    493.90:'B4',
    523.30:'C5',
    554.40:'C5#',
    587.30:'D5',
    622.30:'E5b',
    659.30:'E5',
    698.50:'F5',
    740.00:'F5#',
    784.00:'G5',
    830.60:'G5#',
    880.00:'A5',
    932.30:'B5b',
    987.80:'B5',
    1047.00:'C6',
    1109.0:'C6#',
    1175.0:'D6',
    1245.0:'E6b',
    1319.0:'E6',
    1397.0:'F6',
    1480.0:'F6#',
    1568.0:'G6',
    1661.0:'G6#',
    1760.0:'A6',
    1865.0:'B6b',
    1976.0:'B6',
    2093.0:'C7'
}