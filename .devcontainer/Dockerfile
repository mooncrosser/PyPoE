# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.202.3/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp
RUN apt-get update\
    && apt-get install -y cmake libsodium-dev libunistring-dev \
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

# Re-add if UI work needs to be done
RUN apt-get update\
    && apt-get install -y imagemagick