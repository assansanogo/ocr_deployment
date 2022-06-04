FROM ubuntu:20.04

RUN apt-get update && apt-get install python3 python3-pip -y

RUN apt install tesseract-ocr

RUN pip install pytesseract && pip install pandas

RUN git clone https://github.com/Liberta-Leasing/ocr_deployement.git

CMD ["python3", "-m", "main.py"]