FROM python:3.8.9
MAINTAINER zer0 <osom8979@gmail.com>

ENV RECC_TASK_USER "answer"
ENV RECC_TASK_GROUP "answer"
ENV RECC_TASK_ROOT_DIR "/.answer"
ENV RECC_TASK_WORKSPACE_DIR "$RECC_TASK_ROOT_DIR/workspace"
ENV RECC_TASK_CACHE_DIR "$RECC_TASK_ROOT_DIR/cache"
ENV RECC_TASK_PACKAGE_DIR "$RECC_TASK_ROOT_DIR/package"

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -qq update && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates netbase \
        build-essential ninja-build gcc g++ git curl \
        libffi-dev libgdbm-dev libssl-dev libbz2-dev libexpat-dev \
        libreadline-dev libsqlite3-dev libncurses5-dev liblzma-dev \
        libjemalloc-dev \
        libtesseract-dev tesseract-ocr \
        zlib1g-dev tk-dev \
        xz-utils llvm sudo vim && \
    pip install -U setuptools pip \
        "docker>=4.4.0" \
        "aiodocker>=0.19.1" \
        "aiohttp[speedups]>=3.7.3" \
        "cchardet>=2.1.7" \
        "aiodns>=2.0.0" \
        "brotlipy>=0.7.0" \
        "aiohttp_cors>=0.7.0" \
        "grpcio>=1.36.1" \
        "asyncpg>=0.22.0" \
        "pyyaml>=5.4.1" \
        "psutil>=5.8.0" \
        "pyjwt>=2.0.1" \
        "elasticsearch[async]>=7.0.0,<8.0.0" \
        "uvloop>=0.15.2" \
        "aioredis>=1.3.1" \
        "orjson>=3.5.1" \
        "protobuf>=3.15.6" \
        "numpy>=1.20.2" \
        "colorama>=0.4.4" \
        "coloredlogs>=15.0" \
        "pycryptodome>=3.10.1" \
        "Cython>=0.29.22" && \
    groupadd $RECC_TASK_GROUP && \
    useradd -d $RECC_TASK_ROOT_DIR -m \
            -g $RECC_TASK_GROUP $RECC_TASK_USER && \
    mkdir -p $RECC_TASK_ROOT_DIR \
             $RECC_TASK_WORKSPACE_DIR \
             $RECC_TASK_CACHE_DIR \
             $RECC_TASK_PACKAGE_DIR

WORKDIR /.answer
ENTRYPOINT ["python"]
