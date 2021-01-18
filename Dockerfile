FROM python:3

# We copy just the requirements.txt first to leverage Docker cache
COPY . /inheritance
WORKDIR /inheritance

RUN pip install -r requirements.txt

CMD [ "python", "app/main.py" ]
