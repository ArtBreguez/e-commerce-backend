import requests
from PIL import Image
from io import BytesIO

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def resize_image(image, new_width=100):
    """
    Resize the input image while maintaining the aspect ratio.
    
    Args:
        image (PIL.Image): The input image to resize.
        new_width (int): The desired width for the output image. Defaults to 100.
    
    Returns:
        PIL.Image: The resized image maintaining the original aspect ratio.
    """
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  
    resized_image = image.resize((new_width, new_height))  
    return resized_image

def grayscale_image(image):
    """
    Convert the input image to grayscale.
    
    Args:
        image (PIL.Image): The input image to convert.
    
    Returns:
        PIL.Image: The grayscale version of the input image.
    """
    return image.convert('L') 

def pixels_to_ascii(image):
    """
    Map the grayscale pixels of the image to ASCII characters based on intensity.
    
    Args:
        image (PIL.Image): The grayscale image whose pixels will be converted.
    
    Returns:
        str: A string representing the image in ASCII characters.
    """
    pixels = image.getdata()  
    ascii_str = ''.join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return ascii_str

def convert_image_to_ascii(image, new_width=100):
    """
    Convert an image to an ASCII art representation.
    
    Args:
        image (PIL.Image): The input image to convert.
        new_width (int): The desired width for the output ASCII art. Defaults to 100.
    
    Returns:
        str: A string containing the ASCII art representation of the image.
    """
    image = resize_image(image, new_width)
    image = grayscale_image(image)

    ascii_str = pixels_to_ascii(image)

    img_width = image.width
    ascii_art = "\n".join([ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)])

    return ascii_art

def download_image_from_url(url):
    """
    Download an image from a given URL and return it as a PIL.Image object.
    
    Args:
        url (str): The URL from which to download the image.
    
    Returns:
        PIL.Image or None: The downloaded image as a PIL.Image object, or None if an error occurs.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None

