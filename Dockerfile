FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /spa_table
EXPOSE 8000
WORKDIR /spa_table

COPY ./requirements.txt /spa_table/
COPY . /spa_table

RUN pip3 install -r requirements.txt --no-cache-dir




