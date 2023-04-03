# ticketreader
pip install flask-restful
pip install flask-cors
pip install flask-uploads

pip install python-dotenv

python -m pip install Django
django-admin startproject ticketreader
cd ticketreader
python manage.py runserver
python manage.py migrate
python manage.py startapp grocery
python manage.py makemigrations grocery
python manage.py migrate # despues de makemigrations