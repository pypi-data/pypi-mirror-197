FORMATS = {
    "HEX": 0,
    "RGB": 1,
    "HLS": 2,
    "HSV": 3,
    "ANSI": 4
}
HEX = 0
RGB = 1
HLS = 2
HSV = 3
ANSI = 4
HEX_CODES = [26299, 187, 48059, 0, 47872, 47974, 6732544, 12255419, 12281344, 12255334, 12255232, 8947848, 8939008, 6684859, 12303291, 12303104, 35071, 255, 65535, 6710886, 65280, 65416, 8978176, 16711935, 16746496, 16711816, 16711680, 14540253, 14531328, 8913151, 16777215, 16776960]
ONE_THIRD = 1.0 / 3.0
ONE_SIXTH = 1.0 / 6.0
TWO_THIRDS = 2.0 / 3.0
HEX_TO_ANSI = {
    0x0066BB: 25,
    0x0000BB: 19,
    0x00BBBB: 37,
    0x000000: 16,
    0x00BB00: 34,
    0x00BB66: 35,
    0x66BB00: 70,
    0xBB00BB: 127,
    0xBB6600: 130,
    0xBB0066: 125,
    0xBB0000: 124,
    0x888888: 102,
    0x886600: 94,
    0x6600BB: 55,
    0xBBBBBB: 145,
    0xBBBB00: 142,
    0x0088FF: 33,
    0x0000FF: 21,
    0x00FFFF: 51,
    0x666666: 59,
    0x00FF00: 46,
    0x00FF88: 48,
    0x88FF00: 118,
    0xFF00FF: 201,
    0xFF8800: 208,
    0xFF0088: 198,
    0xFF0000: 196,
    0xDDDDDD: 188,
    0xDDBB00: 178,
    0x8800FF: 93,
    0xFFFFFF: 231,
    0xFFFF00: 226
}
ANSI_TO_HEX = {
    25: 0x0066BB,
    19: 0x0000BB,
    37: 0x00BBBB,
    16: 0x000000,
    34: 0x00BB00,
    35: 0x00BB66,
    70: 0x66BB00,
    127: 0xBB00BB,
    130: 0xBB6600,
    125: 0xBB0066,
    124: 0xBB0000,
    102: 0x888888,
    94: 0x886600,
    55: 0x6600BB,
    145: 0xBBBBBB,
    142: 0xBBBB00,
    33: 0x0088FF,
    21: 0x0000FF,
    51: 0x00FFFF,
    59: 0x666666,
    46: 0x00FF00,
    48: 0x00FF88,
    118: 0x88FF00,
    201: 0xFF00FF,
    208: 0xFF8800,
    198: 0xFF0088,
    196: 0xFF0000,
    188: 0xDDDDDD,
    178: 0xDDBB00,
    93: 0x8800FF,
    231: 0xFFFFFF,
    226: 0xFFFF00
}

def colorConvert(currentFormat: int, destinationFormat: int, color):
    if currentFormat == destinationFormat:
        return color
    if currentFormat > 4 or destinationFormat > 4:
        raise IndexError("Index must not exceed 4")
    formatNames = {
        0: "HEX",
        1: "RGB",
        2: "HLS",
        3: "HSV",
        4: "ANSI"
    }
    usedFormat = f"{formatNames[currentFormat]},{formatNames[destinationFormat]}"
    if usedFormat == "HEX,RGB":
        hexColor = str(color)
        if type(color) is int:
            hexColor = hex(color)[2:]
        while len(hexColor) < 6:
            hexColor = "0" + hexColor
        return tuple(int(hexColor[i:i + 2], 16) for i in (0, 2, 4))
    if usedFormat == "RGB,HEX":
        return "{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
    if usedFormat == "RGB,HLS":
        maxc = max(color[0], color[1], color[2])
        minc = min(color[0], color[1], color[2])
        sumc = (maxc + minc)
        rangec = (maxc - minc)
        l = sumc / 2.0
        if minc == maxc:
            return 0.0, l, 0.0
        if l <= 0.5:
            s = rangec / sumc
        else:
            s = rangec / (2.0 - sumc)
        rc = (maxc - color[0]) / rangec
        gc = (maxc - color[1]) / rangec
        bc = (maxc - color[2]) / rangec
        if color[0] == maxc:
            h = bc - gc
        elif color[1] == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = (h / 6.0) % 1.0
        return tuple(h, l, s)
    if usedFormat == "HLS,RGB":
        h, l, s = color[0], color[1], color[2]
        if s == 0.0:
            return l, l, l
        if l <= 0.5:
            m2 = l * (1.0 + s)
        else:
            m2 = l + s - (l * s)
        m1 = 2.0 * l - m2
        return (_v(m1, m2, h + ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h - ONE_THIRD))
    if usedFormat == "HEX,HLS":
        return colorConvert(RGB, HLS, colorConvert(HEX, RGB, color))
    if usedFormat == "HLS,HEX":
        return colorConvert(RGB, HEX, colorConvert(HLS, RGB, color))
    if usedFormat == "RGB,HSV":
        maxc = max(color[0], color[1], color[2])
        minc = min(color[0], color[1], color[2])
        v = maxc
        if minc == maxc:
            return 0.0, 0.0, v
        s = (maxc - minc) / maxc
        rc = (maxc - color[0]) / (maxc - minc)
        gc = (maxc - color[1]) / (maxc - minc)
        bc = (maxc - color[2]) / (maxc - minc)
        if color[0] == maxc:
            h = bc - gc
        elif color[1] == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = (h / 6.0) % 1.0
        return (h, s, v)
    if usedFormat == "HSV,RGB":
        h, s, v = color[0], color[1], color[2]
        if s == 0.0:
            return (v, v, v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)
        return (0, 0, 0)
    if usedFormat == "HEX,HSV":
        return colorConvert(RGB, HSV, colorConvert(HEX, RGB, color))
    if usedFormat == "HSV,HEX":
        return colorConvert(RGB, HEX, colorConvert(HSV, RGB, color))
    if usedFormat == "HLS,HSV":
        return colorConvert(RGB, HSV, colorConvert(HLS, RGB, color))
    if usedFormat == "HSV,HLS":
        return colorConvert(RGB, HLS, colorConvert(HSV, RGB, color))
    if usedFormat == "HEX,ANSI":
        smallestDifference = [0xFFFFFFF, 0]
        for i in HEX_CODES:
            if smallestDifference[0] > abs(color - i):
                smallestDifference[0] = abs(color - i)
                smallestDifference[1] = i
        return HEX_TO_ANSI[smallestDifference[1]]
    if usedFormat == "ANSI,HEX":
        return ANSI_TO_HEX[color]
    if usedFormat == "RGB,ANSI":
        return colorConvert(HEX, ANSI, colorConvert(RGB, HEX, color))
    if usedFormat == "HLS,ANSI":
        return colorConvert(HEX, ANSI, colorConvert(HLS, HEX, color))
    if usedFormat == "HSV,ANSI":
        return colorConvert(HEX, ANSI, colorConvert(HSV, HEX, color))
    if usedFormat == "ANSI,RGB":
        return colorConvert(HEX, RGB, colorConvert(ANSI, HEX, color))
    if usedFormat == "ANSI,HLS":
        return colorConvert(HEX, HLS, colorConvert(ANSI, HEX, color))
    if usedFormat == "ANSI,HSV":
        return colorConvert(HEX, HSV, colorConvert(ANSI, HEX, color))
    raise IndexError("Please reach me on GitHub @ murjo06 if you ever see this")

def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2 - m1) * hue * 6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRDS:
        return m1 + (m2 - m1) * (TWO_THIRDS - hue) * 6.0
    return m1

def getANSITagRGB(color):
    return f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"