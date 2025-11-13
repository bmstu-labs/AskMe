FROM python:3.12

RUN apt-get update && apt-get install -y curl build-essential

WORKDIR /Askme

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]