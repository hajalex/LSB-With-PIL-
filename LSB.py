from PIL import Image

def hide_message(image_path, message):
    # Open the image at the given path
    image = Image.open(image_path)

    # Convert the message into binary
    binary_message = ''.join(format(ord(msg), '08b') for msg in message)

    # Get the size of the image
    width, height = image.size

    # Set the maximum number of bits to hide in the image
    max_bits = width * height * 3 // 8

    # Check that the message can fit in the image
    if len(binary_message) > max_bits:
        raise Exception("Message is too long to hide in the image")

    # Convert the binary message into a list of digits
    digits = [int(bit) for bit in binary_message]

    # Iterate over the pixels in the image and set the least significant bit
    # of each color component to the next digit of the message
    pixel_index = 0
    for x in range(width):
        for y in range(height):
            if pixel_index < len(digits):
                pixel = list(image.getpixel((x, y)))
                for i in range(3):
                    pixel[i] = (pixel[i] & ~1) | digits[pixel_index]
                    pixel_index += 1
                image.putpixel((x, y), tuple(pixel))

    # Save the new image with the message hidden inside
    image.save(f"{image_path}.hidden.png")

def reveal_message(image_path):
    # Open the image at the given path
    image = Image.open(image_path)

    # Get the size of the image
    width, height = image.size

    # Initialize an empty binary message
    binary_message = ""

    # Iterate over the pixels in the image and extract the least significant
    # bit of each color component to reconstruct the binary message
    for x in range(width):
        for y in range(height):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    # Convert the binary message into ASCII characters
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message

# Hide a message inside an image
hide_message("image.png", "Hello, this is a hidden message!")

# Reveal the message hidden inside an image
message = reveal_message("image.png.hidden.png")
print(message)
