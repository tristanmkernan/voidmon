FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1

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
RUN uv run playwright install --with-deps --no-shell chromium

RUN ["chmod", "+x", "/app/docker-entrypoint.sh"]

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
