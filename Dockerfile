FROM python:3.9
ENV PYTHONUMBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.tx
RUN pip install -r requirements.txt
COPY . /app

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD export DJNAGO_ENV=production
CMD python manage.py runserver 0.0.0.0:8000