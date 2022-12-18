from flask import Flask, jsonify, request
from flask_cors import cross_origin
from dotenv import load_dotenv
import app
import os

server = Flask(__name__)
load_dotenv()


@server.route('/', methods=['POST'])
@cross_origin(origin=os.getenv("APP_CORSSACCES_URL"))
def retrieve():

    # f = open("./file.txt", "w")
    print(request.get_json())
    print(request)
    # f.write(jsonify(request.data))
    # f.close()

    # data_data = request.get_data()
    # print("DATA")
    # for key, value in data_data.items():
    #     print(key, value)

    form_data = request.form
    print("FORM")
    for key, value in form_data.items():
        print(key, value)

    file_data = request.files
    print("FILES")
    for key, value in file_data.items():
        print(key, value)

    print("END")

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
    # images = UploadSet("images", IMAGES)
    # if "image" in request.files:
    #     filename = images.save(request.files["image"])
    #     print(filename)
    # print("No image file found")

    # img = request.files['image']
    # print(img)
    # file_size = img.content_length
    # print(f'File size: {file_size} bytes')

    # # Reading image using OCR
    # text = app.get_img_text(img)

    # print(text)

    # # Retrieving products from the image text
    # data = app.get_products(text)
    # print(data)

    response['msg'] = 'OK'
    response['data'] = {}

    return jsonify(response)


@server.route('/', methods=['GET'])
def error():
    response = {'message': 'Not allowed'}
    return jsonify(response)


if __name__ == '__main__':
    server.run(debug=True)
