"""
Image strings manipulator module
Kirill Kononenko IU7-15
"""

from PIL import Image


def to_ascii(s: str) -> list:
    """Translates string to binary ascii code"""

    result = []
    for let in s:
        bin_let = bin(ord(let))[2:]
        result.append(bin_let)

    return result


def from_ascii(s: str) -> str:
    """Encodes symbol from binary code"""

    return chr(int(s, 2))


def extend(a: list) -> list:
    """Extends symbol to 9-bit length"""

    for i in range(len(a)):
        while len(a[i]) < 9:
            a[i] = '0' + a[i]

    return a


def encode(image: Image.Image, message: str) -> Image.Image:
    """
    Encodes a message into an image by inserting
    symbols in 9-bit binary form using LSB method.
    Encoded sequence ends with symbol '2'.
    """

    data = list(image.getdata())
    ascii_text = extend(to_ascii(message))
    new_data: list = [list(data[i]) for i in range(len(ascii_text) * 3 + 1)]

    l = 0
    for sym in ascii_text:
        current_bit = 0
        for i in range(3):
            for j in range(len(new_data[i + l])):
                encoded_pixel = str(new_data[i + l][j])[:-1] + sym[current_bit]
                new_data[i + l][j] = int(encoded_pixel)
                current_bit += 1
        l += 3

    # Write symbol '2' as ending symbol
    encoded_pixel = str(new_data[l][0])[:-1] + '2'
    new_data[l][0] = int(encoded_pixel)

    # Convert to tuple list
    for i in range(len(new_data)):
        new_data[i] = tuple(new_data[i])
    image.putdata(new_data)

    return image


def decode(image: Image.Image) -> str:
    """Decodes a message from an image"""

    data = image.getdata()
    bin_message = ''
    has_ended = False

    # Get bit sequence from an image
    for i in range(len(data)):
        for j in range(len(data[0])):
            bit = str(data[i][j])[-1:]
            if (bit == '2'):
                has_ended = True
                break
            else:
                bin_message += bit
        if has_ended:
            break

    # Get symbols from the sequence
    message = ''
    for i in range(len(bin_message) // 9):
        sym = ''
        for j in range(9):
            sym += bin_message[9 * i + j]
        message += from_ascii(sym)

    return message


def main():
    img = Image.open("cat.bmp")
    # msg = "Example message"
    # print(decode(img))

    # data = img.getdata()
    # new_data = new_img.getdata()
    #
    # for i in range(len(data)):
    #     if data[i] != new_data[i]:
    #         print("diff!")

    # encode(img, msg)
    # img.save("encat.bmp")
    # print(decode(img))


    # new_img = encode(img, msg)
    # print(decode(new_img))


if __name__ == "__main__":
    main()
