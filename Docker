FROM python:3.8

RUN pip install gunicorn

CMD gunicorn app:app --bind 0.0.0.0:8000
