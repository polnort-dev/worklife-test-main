# Consider using Debian12-Bookworm which has been released in 2023. Should be stable enough.
FROM python:3.11-slim-bookworm
#FROM python:3.11-slim-bullseye
#FROM python:3.11-slim-buster

# Install compilers
RUN apt-get update && apt-get install -y --no-install-recommends \
	curl gcc g++ libffi-dev make && \
	rm -rf /var/lib/apt/lists/*
#	curl -sSL https://install.python-poetry.org/ | POETRY_HOME=/opt/poetry python && \
#    cd /usr/local/bin && \
#    ln -s /opt/poetry/bin/poetry \

# Install Poetry
# Better practice to freeze the poetry version so that the behavior is not depending anymore on future updates
ENV POETRY_VERSION=2.1.1
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock README.md ./

COPY app ./app

RUN poetry config virtualenvs.create false \
    && poetry install && echo "Success"

ENV PATH=/root/.local/bin:$PATH
EXPOSE 80
