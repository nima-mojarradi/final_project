FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . .

CMD python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000