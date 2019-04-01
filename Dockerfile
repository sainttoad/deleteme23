FROM python:3

RUN pip3 install --upgrade pip

ADD app/requirements.txt /tmp/requirements.txt
RUN cd /tmp && pip3 install -r requirements.txt

ADD app /deleteme23
ADD secrets/secrets /secrets

WORKDIR /deleteme23

CMD python3 ./deleteme23.py
