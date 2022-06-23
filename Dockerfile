FROM amazon/aws-lambda-python:3.9

WORKDIR /home/ubuntu

RUN yum clean all

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Paris

RUN yum update -y && yum install -y make curl wget sudo libtool clang git gcc-c++.x86_64 libgl1 libgl1-mesa-glx mesa-libGL ffmpeg libsm6 libxext6 poppler-utils

RUN yum install python3 python3-pip -y

RUN yum install tar

WORKDIR "${LAMBDA_TASK_ROOT}"

COPY install.sh "${LAMBDA_TASK_ROOT}"

RUN chmod +x install.sh

RUN  ./install.sh --target "${LAMBDA_TASK_ROOT}"

RUN git clone https://github.com/Liberta-Leasing/ocr_deployement.git

RUN pip install -r ocr_deployement/requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN rm ocr_deployement/requirements.txt

CMD ["ocr_deployement/lambda_function.lambda_handler"]