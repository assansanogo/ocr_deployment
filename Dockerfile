ARG FUNCTION_DIR="/function"

FROM public.ecr.aws/docker/library/python:buster as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

WORKDIR /home/ubuntu

RUN apt-get update && apt-get install -y

RUN apt-get install -y apt-utils

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Paris

RUN apt-get install python3 python3-pip tesseract-ocr git -y && \
mkdir -p ${FUNCTION_DIR}

RUN git clone https://github.com/Liberta-Leasing/ocr_deployement.git && \
pip install -r ocr_deployement/requirements.txt --target ${FUNCTION_DIR} && \
pip install awslambdaric --target ${FUNCTION_DIR}

RUN  cp ocr_deplyement/lambda_function.py ${FUNCTION_DIR}

FROM public.ecr.aws/docker/library/python:buster

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD ["lambda_function.lambda_handler"]