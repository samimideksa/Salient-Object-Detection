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

RUN python3.6 -m pip install -U pip
RUN python3.6 -m pip install Pillow==5.3.0 matplotlib==2.2.2  numpy==1.15.4  torch==1.0  torchvision==0.2.1  argparse==1.4.0
RUN python3.6 -m pip install grpcio grpcio-tools
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

COPY . /Salient-Object-Detection

WORKDIR /Salient-Object-Detection

EXPOSE 50051

RUN python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Service/inference.proto

