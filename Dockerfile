FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        python3.6 \
        python3.6-dev \
        python3-pip \
        python-setuptools \
        cmake \
        wget \
        curl \
        libsm6 \
        libxext6 \ 
        libxrender-dev

RUN python3.6 -m pip install grpcio grpcio-tools

WORKDIR /tmp

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

COPY . /salient-object-dtection-service

WORKDIR /salient-object-detection-service

EXPOSE 50051

RUN . cd Service && python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. inference.proto

