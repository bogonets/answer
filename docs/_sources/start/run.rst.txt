.. meta::
    :keywords: RUN

.. _doc-start-run:

실행방법
========

이 페이지는 "엔서" 설치후 실행하는 방법에 대하여 정리한 곳입니다.

Docker 실행
-----------

유틸리티 스크립트 다운로드
--------------------------

Docker를 사용하는데 익숙치 않다면 다음 명령으로 스크립트를 다운로드 받습니다.

.. code-block:: bash
    :linenos:

    sudo curl -L "https://raw.githubusercontent.com/bogonets/answer-doc/master/_static/answer-cli" -o /usr/local/bin/answer-cli
    sudo chmod +x /usr/local/bin/answer-cli

스크립드 사용 방법은 다음과 같습니다.

.. code-block:: text
    :linenos:

    Usage: answer-cli [options] {command} {?module}

    Available options are:
      -h, --help     Print this message.
      -y, --yes      Automatic yes to prompts.
      -l, --list     List of options.
      -n, --dry-run  Don’t actually do anything, just show what would be done.
      -v, --verbose  Be more verbose/talkative during the operation.
      --             Stop handling options.

    List of commands:
      images         List images
      logs           View output from containers
      ps             List containers
      pull           Pull service images
      restart        Restart services
      rm             Remove stopped containers
      start          Start services
      stop           Stop services
      run            Create new containers

    List of modules:
      db             Database
      s3             Storage Service
      core           Answer core
      api            Answer api
      web            Answer web

answer-cli config
-----------------

``answer-cli`` 스크립트를 실행하면
``$HOME/.answer/answer-cli.config`` 위치에 환경변수가 함께 저장됩니다.

- ANSWER_DB_PORT
- ANSWER_DB_USER
- ANSWER_DB_PASSWORD
- ANSWER_S3_PORT
- ANSWER_S3_ID
- ANSWER_S3_PW
- ANSWER_CORE_NODE
- ANSWER_CORE_BIND
- ANSWER_CORE_PORT
- ANSWER_CORE_VERBOSE
- ANSWER_CORE_SYNC
- ANSWER_API_PORT
- ANSWER_API_DB_URL
- ANSWER_API_S3_URL
- ANSWER_API_CORE_URL
- ANSWER_WEB_HOST
- ANSWER_WEB_PORT
- ENABLE_GPU
- GPUS
- ENABLE_HOST_NETWORK
- DOCKER_LOGS_TAIL_NUMBER

.. warning:: 특별한 이유가 없다면 위의 값들은 변경하지 않는 것이 좋습니다.

default.json example
--------------------

``$HOME/.answer/core.storage/node/default.json`` 위치에 다음 내용을 저장해야 합니다.

.. code-block:: javascript
    :linenos:

    {
      "logger": {
        "name": "default.logger",
        "sink": "console",
        "arguments": "stdout",
        "generator": "default_color",
        "line_feed": "auto",
        "severity": "notice",
        "auto_flush": true,
        "thread": true
      },
      "socket": {
        "recv_timeout": "4sec",
        "send_timeout": "1sec",
        "recv_number_of_messages": 16,
        "send_number_of_messages": 16,
        "recv_buffer_byte": "32m",
        "send_buffer_byte": "32m",
        "reconnect_time_min": 10,
        "reconnect_time_max": 10
      },
      "inits": [
        {
          "type": "git",
          "arguments": "https://github.com/bogonets/answer-lambda-cv2",
          "branch": "master",
          "auto_update": true,
          "destination": "${STORAGE_PYTHON}/answer-lambda-cv2"
        },
        {
          "type": "git",
          "arguments": "https://github.com/bogonets/answer-lambda-numpy",
          "branch": "master",
          "auto_update": true,
          "destination": "${STORAGE_PYTHON}/answer-lambda-numpy"
        },
        {
          "type": "git",
          "arguments": "https://github.com/bogonets/answer-lambda-preview",
          "branch": "master",
          "auto_update": true,
          "destination": "${STORAGE_PYTHON}/answer-lambda-preview"
        },
        {
          "type": "git",
          "arguments": "https://github.com/bogonets/answer-lambda-rtc",
          "branch": "master",
          "auto_update": true,
          "destination": "${STORAGE_PYTHON}/answer-lambda-rtc"
        }
      ],
      "immutable": true
    }

엔서 이미지 다운로드
--------------------

다음과 같이 실행 하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli pull

특정 모듈만 다운로드 받고 싶다면 다음과 같이 모듈명을 추가하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli pull core

엔서 실행
---------

다음과 같이 실행 하면 됩니다.
이 때 "엔서"는 서비스로 실행됩니다.

.. code-block:: bash
    :linenos:

    answer-cli run

마찬가지로, 특정 모듈만 실행하고 싶다면 모듈명을 추가하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli run core

엔서 중지
---------

이미 작동중인 서비스가 존재할 때 "엔서"를 중지시키고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli stop

정지된 서비스를 재기동 시키고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli start

위의 ``stop`` 명령과 ``start`` 명령을 한 번에 실행하고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli restart

엔서 제거
---------

엔서의 설정파일 및 컨테이너를 제거하고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli rm

.. warning:: 이렇게 제거할 경우 이미 저장된 설정 정보가 유실됩니다.

엔서 로그 확인
--------------

엔서의 로그 메시지를 확인하고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli logs core

.. note:: ``logs`` 명령은 ``all`` 모듈명을 읽지 못합니다.
          ``core``, ``api``, ``web`` 중 하나를 사용해 주세요.

엔서 이미지 확인
----------------

현재 다운받은 엔서 이미지를 확인하고 싶다면 다음과 같이 실행하면 됩니다.

.. code-block:: bash
    :linenos:

    answer-cli images

서비스 기동 상태 확인
---------------------

엔서를 실행했다면 다음의 명령으로 상태정보를 확인할 수 있습니다.

.. code-block:: bash
    :linenos:

    answer-cli ps

