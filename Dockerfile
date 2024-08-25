FROM python:3.10-slim

RUN pip install poetry

WORKDIR /IoC-python

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY ioc ./ioc
COPY example ./example

ENV PYTHONPATH "${PYTHONPATH}:/IoC-python"

RUN poetry install

CMD ["poetry", "run", "python", "./example/main.py"]

