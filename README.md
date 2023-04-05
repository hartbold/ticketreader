# ticketreader

pip install opencv-python
-- install https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe
pip install pytesseract
pip install openai

## DJANGO 
pip install python-dotenv

python -m pip install Django
django-admin startproject ticketreader
cd ticketreader
python manage.py runserver
python manage.py migrate
python manage.py startapp grocery
python manage.py makemigrations grocery
python manage.py migrate # despues de makemigrations

## FLASK (old)
pip install flask-restful
pip install flask-cors
pip install flask-uploads
