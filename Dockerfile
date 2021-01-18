FROM python:3

COPY . /inheritance
WORKDIR /inheritance

RUN pip install -r requirements.txt

CMD [ "python", "app/main.py" ]
