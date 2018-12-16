FROM python:alpine3.7

ADD ./ /Stix-2.0-Editor

RUN pip3 install -r /Stix-2.0-Editor/requirements.txt

CMD ["python3 /Stix-2.0-Editor/Main.py"]