FROM python:3

RUN pip3 install --upgrade pip

ADD app/requirements.txt /tmp/requirements.txt
RUN cd /tmp && pip3 install -r requirements.txt

ADD app /stt
ADD secrets/secrets /secrets

WORKDIR /stt

CMD python3 ./stt.py