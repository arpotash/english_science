FROM python:3.9

WORKDIR /usr

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt
COPY . /usr/src

CMD ["python", "src/main.py"]
