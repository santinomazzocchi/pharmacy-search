FROM python:3.6
ADD . /code
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD [ "python", "-u", "app.py" ]
