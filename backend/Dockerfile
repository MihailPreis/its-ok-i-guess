FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py

RUN pip3 install -r requirements.txt

EXPOSE 5001

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]