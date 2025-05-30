FROM python:3.12.7-alpine3.20
LABEL maintainer="dsahalatyi@gmail.com"

ENV \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	VIRTUAL_ENV=/venv
ENV \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_VIRTUALENVS_IN_PROJECT=false \
	POETRY_NO_INTERACTION=1 \
	POETRY_VERSION=2.1.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml ./

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV \
	&& . $VIRTUAL_ENV/bin/activate \
	&& poetry install --no-root

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]