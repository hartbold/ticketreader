from flask import Flask, jsonify, request
from flask_cors import cross_origin
from dotenv import load_dotenv
import utils_old
import os

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = './img/'

load_dotenv()

@server.route('/', methods=['POST'])
@cross_origin(origin=os.getenv("APP_CORSSACCES_URL"))
def retrieve():

    # print("END")

    # img = form_data["image"]
    # return print(type(img))

    response = {
        'status': 1,
        'msg': '',
        'data': ''
    }

    # hash control
    hash = request.headers.get('hash')
    if hash != os.getenv("SERVER_APIKEY"):
        response['status'] = 0
        response['msg'] = 'Error'
        return jsonify(response)

    # image retrieve
    img_stream = request.files.get("image")
    filename = img_stream.filename
    filepath = os.path.join(server.config['UPLOAD_FOLDER'], filename)

    if not img_stream or filename == '' or not utils_old.allowed_file(img_stream):
        response['status'] = 0
        response['msg'] = 'Error file'
        return jsonify(response)
    
    # todo ok save the file
    img_stream.save(filepath)

    # Reading image using OCR
    text = utils_old.get_img_text(filepath)

    # Retrieving products from the image text
    data = utils_old.get_products(text)

    response['msg'] = 'OK'
    response['data'] = {
        "text": text,
        "items": data
    }

    os.remove(filepath)

    return jsonify(response)


@server.route('/', methods=['GET'])
def error():
    response = {'message': 'Not allowed'}
    return jsonify(response)


if __name__ == '__main__':
    server.run(debug=True)
