.. meta::
    :keywords: INSTALL

.. _doc-start-install:

설치방법
========

이 페이지는 "엔서"를 설치하기 위한 방법에 대하여 정리한 곳입니다.

설치하기에 앞서
---------------

"엔서"는 `Ubuntu <https://ubuntu.com/>`_ 플랫폼과 `Docker <https://www.docker.com/>`_ 도구를 기본으로 배포합니다.

.. note:: 현재는 도커(Docker)를 사용한 배포만 지원합니다.
          플랫폼별 배포는 차 후 지원 계획에 포함되어 있습니다.

또한 설치하기에 앞서 CPU가 "가상화 기술 (Virtualization Technology)"을 지원하는지 확인해야 합니다.
CPU 벤더에 따라 가상화을 지칭하는 기술명이 다릅니다.

- Intel VT
- AMD-V

"BIOS 유틸리티" 또는 "CPU 정보" 도구 등을 활용하여 확인할 수 있습니다.

- 윈도우를 사용한다면 ``작업 관리자 > 성능 탭 > CPU`` 에서 확인할 수 있습니다.
- 리눅스를 사용한다면 ``lscpu | grep Virtualization`` 로 확인할 수 있습니다.

Docker 설치
-----------

도커는 응용 프로그램을 컨테이너에 격리시키는 자동화 도구 입니다.

.. note:: 설치 방법이 변경될 수 있으므로
          공식 홈페이지에서 최신 정보를 확인해 주세요.

- `Install Docker Desktop on Mac <https://docs.docker.com/docker-for-mac/install/>`_
- `Install Docker Desktop on Windows <https://docs.docker.com/docker-for-windows/install/>`_
- `Install Docker Engine on Ubuntu <https://docs.docker.com/engine/install/ubuntu/>`_

자세한 내용은 `Get Docker <https://docs.docker.com/get-docker/>`_ 페이지에서 확인할 수 있습니다.
만약, 우분투(x86_64/amd64)를 사용할경우 아래의 명령으로 설치할 수 있습니다.

.. code-block:: bash
    :linenos:

    ## Uninstall old versions
    sudo apt-get remove docker docker-engine docker.io containerd runc

    ## Set up the repository
    sudo apt-get update
    sudo apt-get install \
         apt-transport-https \
         ca-certificates \
         curl \
         gnupg-agent \
         software-properties-common

    ## Add Docker’s official GPG key:
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    ## Verify that you now have the key with the fingerprint
    sudo apt-key fingerprint 0EBFCD88

    ## Set up the stable repository.
    sudo add-apt-repository \
         "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
         $(lsb_release -cs) \
         stable"

    ## Install Docker Engine
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io

    ## Add docker group
    sudo usermod -aG docker your-user

    ## Verify that Docker Engine is installed correctly by running the hello-world image.
    sudo docker run hello-world

Docker Compose 설치
-------------------

`Docker Compose <https://docs.docker.com/compose/>`_ 는 여러 컨테이너 애플리케이션을 정의하고 실행하기위한 도구입니다.
자세한 설치 방법은 `Install Docker Compose <https://docs.docker.com/compose/install/>`_ 페이지를 확인해 주세요.

리눅스를 사용할경우 아래의 명령으로 간단히 설치할 수 있습니다.

.. code-block:: bash
    :linenos:

    sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

(선택) NVIDIA 그래픽 드라이버 지원
----------------------------------

GPGPU를 위한 CUDA지원을 "엔서"에 적용할 수 있습니다.

.. warning:: "NVIDIA 그래픽 드라이버 지원"은 현재 리눅스 플랫폼만 지원됩니다.
             Docker 지원을 위해 `nvidia-docker <https://nvidia.github.io/nvidia-docker/>`_ 가 필요하기 때문입니다.
             지원 현황은 해당 사이트를 확인해 주세요.

이를 위해 우선 `NVIDIA 그래픽 드라이버 <https://www.nvidia.co.kr/Download/index.aspx?lang=kr>`_ 를 설치해야 합니다.
해당 사이트를 통해 설치를 진행해야 합니다.

.. note:: `CUDA Toolkit <https://developer.nvidia.com/cuda-toolkit>`_ 를 설치해도
          그래픽 드라이버를 함께 설치할 수 있습니다.

그 후 `nvidia-docker <https://nvidia.github.io/nvidia-docker/>`_ 를 설치합니다.

.. note:: 설치 방법이 변경될 수 있으므로
          공식 홈페이지에서 최신 정보를 확인해 주세요.

만약, 우분투를 사용할경우 아래의 명령으로 설치할 수 있습니다.

.. code-block:: bash
    :linenos:

    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
        sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
        sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    sudo systemctl restart docker

(선택) nvidia-docker-compose 설치
---------------------------------

Docker-Compose 를 사용할 경우 NVIDIA 그래픽 드라이버가 연결되지 않을 수 있다.
이 경우 사용할 수 있는 몇가지 방법이 있다.

- 전체 이미지를 수동으로 실행
- :download:`Bash Script </_static/answer-cli>` 작성
- Docker의 ``daemon.json`` 파일에 ``runtimes`` 설정 추가
- `nvidia-docker-compose <https://github.com/eywalker/nvidia-docker-compose>`_ 설치

이 중 nvidia-docker-compose 를 설치하는 방법은 아래와 같습니다.

.. code-block:: bash
    :linenos:

    pip install nvidia-docker-compose

다음과 같이 사용할 수 있습니다.

.. code-block:: bash
    :linenos:

    docker-compose -f docker-compose-gpu.yaml ...
    ## or
    nvidia-docker-compose ...

.. warning:: 이 방법은 비공식 입니다.

엔서 다운로드
-------------

엔서는 `Docker Hub <https://hub.docker.com/>`_ 공식 사이트에 배포하고 있습니다.
각각의 이미지는 아래의 링크를 참조하세요.

- `bogonets/answer-core <https://hub.docker.com/r/bogonets/answer-core>`_
- `bogonets/answer-api <https://hub.docker.com/r/bogonets/answer-api>`_
- `bogonets/answer-web <https://hub.docker.com/r/bogonets/answer-web>`_

최신 버전을 받고 싶다면 아래의 명령을 입력하면 됩니다.

.. code-block:: bash
    :linenos:

    docker pull bogonets/answer-core
    docker pull bogonets/answer-api
    docker pull bogonets/answer-web
