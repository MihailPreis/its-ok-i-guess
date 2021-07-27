FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY public/ public/

RUN pip3 install -r requirements.txt

EXPOSE 42312

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]