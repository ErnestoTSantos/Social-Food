FROM python:3.12

RUN apt update
RUN apt install -y git

WORKDIR /app

RUN useradd appuser && chown appuser ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY --chown=appuser poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY --chown=appuser . ./