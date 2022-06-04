FROM ubuntu:20.04

RUN apt-get update && apt-get install python3 python3-pip -y

RUN apt-get -y install git

RUN apt-get install -y apt-utils

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Paris

RUN apt install tesseract-ocr -y

COPY test_image1.jpg .

COPY test_image3.jpg .

RUN git clone https://github.com/Liberta-Leasing/ocr_deployement.git

RUN pip install -r ocr_deployement/requirements.txt

RUN rm ocr_deployement/requirements.txt

CMD ["python3", "ocr_deployement/main.py"]