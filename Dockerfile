FROM python:3.6.9
COPY . /app
WORKDIR /app
RUN pip install pipenv && pipenv install --system
CMD gunicorn --bind 0.0.0.0:$PORT --workers=5 --timeout=60 bot.wsgi:application
