FROM python:3.8
ADD . /the-green
WORKDIR /the-green

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False

RUN pip install -U pip pipenv
RUN pipenv install --system --deploy

RUN python manage.py collectstatic --noinput

# EXPOSE 5000

CMD gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
