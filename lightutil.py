def color(hexa):    
    hexa = hexa.lstrip("#")
    return [0x7e, 0x07, 0x05, 0x03, int(hexa[0:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16), 0x00, 0xef]


def bytes_to_rgb(arr):    
    # bytearr
    # [0x7e, 0x07, 0x05, 0x03, int(hexa[0:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16), 0x00, 0xef]
    # We need parts 4, 5, 6 to make the RGB value
    new_bytes = arr[4:6]
    r = int(new_bytes[0], 16)
    g = int(new_bytes[1], 16)
    b = int(new_bytes[2], 16)
    return { r, g, b }
