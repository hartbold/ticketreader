import numpy as np
import cv2
import pytesseract
import openai
import os

pytesseract.pytesseract.tesseract_cmd = os.getenv('PATH_TESSERACT') 

def get_img_text(imgpath):

    img = cv2.imread(imgpath)


    #  img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.resize(img, None, fx=2, fy=2)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1,1), np.uint8)
    #  img = cv2.dilate(img, kernel, iterations=1)
    #  img = cv2.erode(img, kernel, iterations=1)

    #  img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.imwrite(imgpath, img)

    # for psm in range(6,13+1):
    #    config = '--oem 3 --psm %d' % psm
    #    txt = pytesseract.image_to_string(img, config = config, lang='cat')
    #    print('psm ', psm, ':',txt)

    config = '--oem 3 --psm %d' % 6
    txt = pytesseract.image_to_string(img, config = config, lang='cat')

    # Convert the image to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # creating Binary image by selecting proper threshold
    # binary_image = cv2.threshold(gray ,130,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Inverting the image
    # inverted_bin = cv2.bitwise_not(binary_image)
    # Some noise reduction
    # kernel = np.ones((2, 2), np.uint8)
    # processed_img = cv2.erode(inverted_bin, kernel, iterations=1)
    # processed_img = cv2.dilate(processed_img, kernel, iterations=1)
    # REad text
    # text = pytesseract.image_to_string(gray)
    return txt

def generate_prompt(text):
    # @TODO optimizar el prompt para que no gaste tantos tokens
    # return f'Identifica de el siguiente tiquet de compra los items y devuélvelos en un objeto json con los atributos: cantidad, nombre y precio. El ticket de compra empieza después de los hashtags "###" y termina con la misma marca.\n\nTicket de compra:\n###{text}\n###";'
    # return f'Identify from this purchase ticket all the items. The ticket is between two hashtag marks that define the start and end of the ticket. All the items must be returned in JSON format with the attributes "quatinty", "item", "price". The ticket is in catalan or spanish. :\nSTART ###\n{text}\n### END\n";'
    return f'Recupera els productes del tiquet en un objecte JSON amb les claus "producte","nom_simplificat", "quantitat" i "preu" per cada producte. Els productes poden vindre mal escrits, corregeix-los a la clau "producte". El tiquet és:\n{text}'

def get_products(ticket_text):
    akey = os.getenv("OPENAI_SKEY")
    openai.api_key = akey
    openai.organization = os.getenv("OPENAI_ORGANIZATION")

    '''
    response = openai.Completion.create(
        model=os.getenv("OPENAI_MODEL"),
        prompt=generate_prompt(ticket_text),
        temperature=1,
        max_tokens=2000,
        n=1,
    )
    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ets un interpret de text de tiquets de compra"},
            {"role": "user", "content": generate_prompt(ticket_text)}
        ],
    )

    valores = response["choices"][0]["message"]["content"]

    return valores

def allowed_file(imgstream):

    valid = True
    extvalidas = [".jpg", ".jpeg", ".png"]

    fpath = os.path.splitext(imgstream.name)
    fext = (fpath[len(fpath)-1]).lower()

    # Comprobar extension
    try:
        if extvalidas.index(fext) < 0:
            print("Not in ext")
            valid = False
    except:
        print("Wrong ext")
        valid = False


    # imgstream.filename
    if imgstream.size > 52428800:
        print("File size bigger")
        valid = False

    return valid