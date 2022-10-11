FROM python:3.9.14
MAINTAINER zer0 <osom8979@gmail.com>

RUN pip install -U setuptools pip && \
    pip install -U recc && \
    mkdir /recc

WORKDIR /
ENTRYPOINT ["python", "-m", "recc", "core", "--local-storage", "/recc"]
