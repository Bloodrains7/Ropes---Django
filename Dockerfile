FROM python:3.9

RUN apt update
RUN apt-get install cron -y

ENV PYTHONUMBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

RUN python manage.py makemigrations auth
RUN python manage.py makemigrations udigital
RUN python manage.py migrate

RUN python manage.py loaddata udigital/fixtures/1_phonenumber.json
RUN python manage.py loaddata udigital/fixtures/2_user.json
RUN python manage.py loaddata udigital/fixtures/3_post.json
RUN python manage.py loaddata udigital/fixtures/4_comment.json

#django-crontab logfile
RUN mkdir /cron
RUN touch /cron/django_cron.log

CMD export DJNAGO_ENV=production
CMD service cron start && python manage.py runserver 0.0.0.0:8000

RUN python manage.py crontab add