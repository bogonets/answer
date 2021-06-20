.. meta::
    :keywords: TROUBLESHOOTING

.. _doc-etc-troubleshooting:

문제 해결
=========

문제 해결 가이드를 제공합니다.

Docker 실행시 libnvidia-tls.so 라이브러리를 찾을 수 없습니다
------------------------------------------------------------

Docker 실행시 다음과 같은 에러 메시지가 출력될 수 있습니다.

.. error::
    docker: Error response from daemon: OCI runtime create failed: container_linux.go:349: starting container process caused "process_linux.go:449: conatiner init caused \"process_linux.go:432: running prestart hook 0 caused \\\"error running hook: exit status 1, stdout: , stderr: nvidia-container-cli: detection error: open failed: /usr/lib/x86_64-linux-gnu/libnvidia-tls.so.450.36.06: no such file or directory

``libnvidia-tls.so`` 라이브러리를 찾을 수 없는 경우 발생됩니다.
:ref:`nvidia-docker <doc-start-install>` 를 다시 설치해야 합니다.

템플릿 불러오기 실패
--------------------

"그래프" 페이지에서 "템플릿 불러오기 실패" 라는 메시지가 출력될 경우 엔서의 코어 모듈을 재실행 해야 합니다.

엔서가 작동하지 않습니다
------------------------

프로그램 오류로 엔서가 작동하지 않을 경우 엔서를 제거한 후 다시 실행해야 합니다.
방법은 :ref:`실행 <doc-start-run>` 페이지의 가이드 에서 확인할 수 있습니다.

엔서 버전 변경 후 그래프가 정상적으로 호출되지 않습니다
-------------------------------------------------------

엔서 버전 변경 후 실행 했을 때 그래프 설정 페이지에서 그래프 불러오기 실패 알림창이 뜨며, 그래프가 불러지지 않을 수 있습니다.

아래 순서대로 컨테이너 및 데이터베이스를 삭제한 후 다시 실행해야 합니다.

.. code-block:: bash
    :linenos:

    answer-cli stop
    answer-cli rm
    answer-cli run

엔서 실행 후 일정시간이 지나면 마우스와 키보드가 정상적으로 작동하지 않습니다
-----------------------------------------------------------------------------

/etc/logrotate.d/ 위치에 docker-container 파일을 생성하고 아래 내용을 추가합니다.

.. code-block:: bash
    :linenos:

    /var/lib/docker/containers/*/*.log {
      rotate 7
      daily
      compress
      missingok
      delaycompress
      copytruncate
    }

추가 후 아래 명령어를 실행합니다.

.. code-block:: bash
    :linenos:

    logrotate -fv /etc/logrotate.d/docker-container

