import cv2
import pytesseract
import openai
import numpy as np
import os
import re
from dotenv import load_dotenv


def get_img_text(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # creating Binary image by selecting proper threshold
    # binary_image = cv2.threshold(gray ,130,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Inverting the image
    # inverted_bin = cv2.bitwise_not(binary_image)
    # Some noise reduction
    # kernel = np.ones((2, 2), np.uint8)
    # processed_img = cv2.erode(inverted_bin, kernel, iterations=1)
    # processed_img = cv2.dilate(processed_img, kernel, iterations=1)
    # REad text
    text = pytesseract.image_to_string(gray)
    return text


def generate_prompt(text):
    # @TODO optimizar el prompt para que no gaste tantos tokens
    # return f'Identifica de el siguiente tiquet de compra los items y devuélvelos en un objeto json con los atributos: cantidad, nombre y precio. El ticket de compra empieza después de los hashtags "###" y termina con la misma marca.\n\nTicket de compra:\n###{text}\n###";'
    return f'Identify from this purchase ticket all the items. The ticket is between two hashtag marks that define the start and end of the ticket. All the items must be returned in JSON format with the attributes "quatinty", "item", "price". The ticket is in catalan or spanish. :\nSTART ###\n{text}\n### END\n";'



def get_products(ticket_text):
    akey = os.getenv("OPENAI_SKEY")
    openai.api_key = akey

    response = openai.Completion.create(
        model=os.getenv("OPENAI_MODEL"),
        prompt=generate_prompt(ticket_text),
        temperature=1,
        max_tokens=2000,
        n=1,
    )

    valores = response["choices"][0]["text"]

    return valores

# Programa


load_dotenv()

# Loading image using OpenCV
img = cv2.imread('./img/ticket0.JPEG')
# Reading image using OCR
text = get_img_text(img)

print(text)

# Retrieving products from the image text
products = get_products(text)
print(products)
