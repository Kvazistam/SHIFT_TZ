FROM python:3.11
EXPOSE 8000
RUN apt-get update && apt-get install -y \
    curl \
    git

RUN python -m pip install --user pipx

ENV PATH="/root/.local/bin:$PATH"

RUN pipx install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction

COPY . .


CMD ["poetry", "run", "python", "main.py"]
