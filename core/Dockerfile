FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
MAINTAINER zer0 <osom8979@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -qq update && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y --no-install-recommends \
        software-properties-common ca-certificates netbase build-essential ninja-build \
        xorg-dev libglu1-mesa-dev libjemalloc-dev \
        libffi-dev libgdbm-dev libssl-dev libbz2-dev libexpat-dev \
        libreadline-dev libsqlite3-dev libncurses5-dev liblzma-dev \
        libtesseract-dev tesseract-ocr \
        zlib1g-dev tk-dev xz-utils llvm git gcc g++ gdb curl wget sudo vim

RUN mkdir /pysrc /pybin && \
    curl -s -L "https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz" | \
        tar xzf - --strip-components=1 -C /pysrc && \
    cd /pysrc && \
    CFLAGS="-I/opt/X11/include -fPIC" \
    LDFLAGS="-L/opt/X11/lib -Wl,-rpath,/pybin/lib" \
    ./configure --enable-shared --enable-optimizations --prefix=/pybin && \
    make -j2 install && \
    update-alternatives --install /usr/bin/python python "/pybin/bin/python3.7" 10 && \
    update-alternatives --install /usr/bin/pip pip "/pybin/bin/pip3.7" 10 && \
    pip install -U setuptools pip && \
    pip install bogoanswer && \
    rm -rf /pysrc

WORKDIR /
ENTRYPOINT [ "python", "-m", "recc" ]

