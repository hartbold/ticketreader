from flask import Flask, jsonify
from flask import request
from dotenv import load_dotenv
import app as util
import os

app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['POST'])
def retrieve():



    # 

    # # Loading image using OpenCV
    # img = cv2.imread('./img/ticket0.JPEG')
    # # Reading image using OCR
    # text = get_img_text(img)

    # print(text)

    # # Retrieving products from the image text
    # products = get_products(text)
    # print(products)

    data = request.form.get("hola")
    print(request.get_json())

    response = {
        'ip' : request.remote_addr,
        'request' : data,
        'prompt': util.generate_prompt("TEST")
    }
    return jsonify(response), {"Access-Control-Allow-Origin": os.getenv("APP_CORSSACCES_URL")}

@app.route('/', methods=['GET'])
def error():
    response = {'message': 'Not allowed'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()