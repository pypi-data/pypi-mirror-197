CHARLIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 
'v', 'w', 'x', 'y', 'z', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']
VA2SY = dict(enumerate(CHARLIST))
SY2VA = dict(map(reversed, VA2SY.items()))


def encode(string, base):

    integer = int.from_bytes(string.encode("utf-8"), byteorder = "big")
    array = []

    while integer:
        integer, value = divmod(integer, base)
        array.append(VA2SY[value])

    return ''.join(reversed(array))
    
def decode(string, base):

    integer = 0

    for character in string:
        value = SY2VA[character]
        integer *= base
        integer += value

    return integer.to_bytes(((integer.bit_length() + 7) // 8), byteorder = "big").decode("utf-8")