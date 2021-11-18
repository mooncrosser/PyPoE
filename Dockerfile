ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-bullseye

### Install ooz from Zao
RUN export DEBIAN_FRONTEND=noninteractive\
    && apt-get update\
    && apt-get install -y cmake libsodium-dev libunistring-dev\
    && cd /tmp/\
    && git clone https://github.com/zao/ooz.git\
    && cd ooz/\
    && cmake .\
    && cmake --build .\
    && cp ooz /usr/local/bin\
    && cd /\
    && rm -rf /tmp/ooz/\
    && apt-get -y purge cmake libsodium-dev libunistring-dev\
    && apt-get -y autoremove\
    && apt-get -y autoclean

### Install imagemagick for image manipulation
RUN export DEBIAN_FRONTEND=noninteractive\
    && apt-get update\
    && apt-get install -y imagemagick

### Install pypoe
ARG PYPOE_TAG=dev
COPY . /pypoe
WORKDIR /pypoe
RUN pip install --upgrade pip\
    && pip install -U pip setuptools\
    && pip install -U -r test_requirements.txt\
    && pip install -U -e .[cli]\
    && mkdir /output\
    && pypoe_exporter config set out_dir /output\
    && mkdir /tmp/pypoe-temp\
    && pypoe_exporter config set temp_dir /tmp/pypoe-temp\
    && mkdir /poe-data\
    && pypoe_exporter config set ggpk_path /poe-data\
    && pypoe_exporter setup perform

WORKDIR /output

VOLUME [ "/poe-data", "/output" ]

ENTRYPOINT [ "pypoe_exporter" ]