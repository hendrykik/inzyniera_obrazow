"""Function definitions that are used in LSB steganography."""
from matplotlib import pyplot as plt
import numpy as np
import binascii
import cv2 as cv
import math
plt.rcParams["figure.figsize"] = (18,10)


def encode_as_binary_array(msg):
    """Encode a message as a binary string."""
    msg = msg.encode("utf-8")
    msg = msg.hex()
    msg = [msg[i:i + 2] for i in range(0, len(msg), 2)]
    msg = [ "{:08b}".format(int(el, base=16)) for el in msg]
    return "".join(msg)


def decode_from_binary_array(array):
    """Decode a binary string to utf8."""
    array = [array[i:i+8] for i in range(0, len(array), 8)]
    if len(array[-1]) != 8:
        array[-1] = array[-1] + "0" * (8 - len(array[-1]))
    array = [ "{:02x}".format(int(el, 2)) for el in array]
    array = "".join(array)
    result = binascii.unhexlify(array)
    return result.decode("utf-8", errors="replace")


def load_image(path, pad=False):
    """Load an image.
    
    If pad is set then pad an image to multiple of 8 pixels.
    """
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    if pad:
        y_pad = 8 - (image.shape[0] % 8)
        x_pad = 8 - (image.shape[1] % 8)
        image = np.pad(
            image, ((0, y_pad), (0, x_pad) ,(0, 0)), mode='constant')
    return image


def save_image(path, image):
    """Save an image."""
    plt.imsave(path, image) 


def clamp(n, minn, maxn):
    """Clamp the n value to be in range (minn, maxn)."""
    return max(min(maxn, n), minn)


def hide_message(image, message, nbits=1):
    """Hide a message in an image (LSB).
    
    nbits: number of least significant bits
    """
    nbits = clamp(nbits, 1, 8)
    shape = image.shape
    image = np.copy(image).flatten()
    if len(message) > len(image) * nbits:
        raise ValueError("Message is to long :(")
    
    chunks = [message[i:i + nbits] for i in range(0, len(message), nbits)]
    for i, chunk in enumerate(chunks):
        byte = "{:08b}".format(image[i])
        new_byte = byte[:-nbits] + chunk
        image[i] = int(new_byte, 2)
        
    return image.reshape(shape)


def reveal_message(image, nbits=1, length=0):
    """Reveal the hidden message.
    
    nbits: number of least significant bits
    length: length of the message in bits.
    """
    nbits = clamp(nbits, 1, 8)
    shape = image.shape
    image = np.copy(image).flatten()
    length_in_pixels = math.ceil(length/nbits)
    if len(image) < length_in_pixels or length_in_pixels <= 0:
        length_in_pixels = len(image)
    
    message = ""
    i = 0
    while i < length_in_pixels:
        byte = "{:08b}".format(image[i])
        message += byte[-nbits:]
        i += 1
        
    mod = length % -nbits
    if mod != 0:
        message = message[:mod]
    return message

# original_image = load_image("images/spanish.png")  # Wczytanie obrazka
# message = "Stół z powymaławanymi nogami..." 
# n = 1  # liczba najmłodszych bitów używanych do ukrycia wiadomości

# message = encode_as_binary_array(message)  # Zakodowanie wiadomości jako ciąg 0 i 1
# image_with_message = hide_message(original_image, message, n)  # Ukrycie wiadomości w obrazku

# save_image("images/image_with_message.png", image_with_message)  # Zapisanie obrazka w formacie PNG

# image_with_message_png = load_image("images/image_with_message.png")  # Wczytanie obrazka PNG

# secret_message_png = decode_from_binary_array(
#     reveal_message(image_with_message_png, nbits=n, length=len(message)))  # Odczytanie ukrytej wiadomości z PNG

# print(secret_message_png)

def hide_message_in_container(container, message, n):
    message = encode_as_binary_array(message)  # Zakodowanie wiadomości jako ciąg 0 i 1
    container_with_message = hide_message(container, message, n)  # Ukrycie wiadomości w kontenerze
    return container_with_message
    

def reveal_message_in_container(container_with_message, n, length):
    secret_message = decode_from_binary_array(reveal_message(container_with_message, nbits=n, length=length))  # Odczytanie ukrytej wiadomości
    return secret_message


def zakoduj(img, mess, n):
    original_image = load_image(img)  # Wczytanie obrazka
    message = mess

    message = encode_as_binary_array(message)  # Zakodowanie wiadomości jako ciąg 0 i 1
    image_with_message = hide_message(original_image, message, n)  # Ukrycie wiadomości w obrazku

    save_image("images/image_with_message.png", image_with_message)  # Zapisanie obrazka w formacie PNG

def dekoduj(img, message, n):
    image_with_message_png = load_image("images/image_with_message.png")  # Wczytanie obrazka PNG

    secret_message_png = decode_from_binary_array(
        reveal_message(image_with_message_png, nbits=n, length=len(message)))  # Odczytanie ukrytej wiadomości z PNG

    print(secret_message_png)

img = "images/spanish.png"
mess = "Stół bez nóg"
n = 1

zakoduj(img, mess, n)
dekoduj(img, mess, n)