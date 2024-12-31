FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# RUN apt-get update
# RUN apt-get install -y \
#     libmagic-dev \
#     libjpeg-dev \
#     zlib1g-dev \
#     libffi-dev \
#     gfortran \
#     libopenblas-dev

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY .env.prod .env

RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]

ENTRYPOINT [ "/code/docker-entrypoint.sh" ]
