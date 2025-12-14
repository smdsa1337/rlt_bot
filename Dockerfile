FROM python:3.13-alpine

ENV \
   POETRY_NO_INTERACTION=1 \
   POETRY_VIRTUALENVS_CREATE=false \
   PYTHONFAULTHANDLER=1 \
   PYTHONUNBUFFERED=1 \
   PYTHONHASHSEED=random \
   PIP_NO_CACHE_DIR=off \
   PIP_DISABLE_PIP_VERSION_CHECK=on \
   PIP_DEFAULT_TIMEOUT=100

WORKDIR /code
COPY . /code/

RUN pip install poetry pip-autoremove && \
   poetry config virtualenvs.create false && \
   poetry install --no-cache --no-root && \
   pip-autoremove poetry pip-autoremove -y
RUN pip install requests

CMD python3 src/srv.py
