FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONUNBUFFERED=1

# NOTE: won't work on alpine
# RUN apt-get update
# RUN apt-get install -y \
#     libmagic-dev \
#     libjpeg-dev \
#     zlib1g-dev \
#     libffi-dev \
#     gfortran \
#     libopenblas-dev

ADD . /app

WORKDIR /app

COPY .env.prod .env

RUN uv sync --frozen

RUN ["chmod", "+x", "/app/docker-entrypoint.sh"]

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
