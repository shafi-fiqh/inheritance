FROM python:3

COPY . /inheritance
WORKDIR /inheritance

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN python -m venv /inheritance_vm 
RUN source /inheritance_vm/bin/activate 
RUN pip install -r requirements.txt

# Set environment variable
ARG PORT
ENV PORT=$PORT

# Run the application
CMD gunicorn main:app 0.0.0.0:$PORT