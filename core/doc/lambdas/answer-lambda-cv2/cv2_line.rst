.. meta::
	:keywords: CV2

.. role:: raw-html(raw)
	:format: html

cv2_line
=============================

두 점을 연결하는 선분을 그린다.

입력 슬롯
---------

* **source**

* **lines**

출력 슬롯
---------

* **result**

속성 목록
---------

* **Line color**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + color + True     + 0,0,0         |
+-----------------+-------+----------+---------------+

선분의 색상.

* **Line thickness**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + int   + True     + 1             |
+-----------------+-------+----------+---------------+

선분의 두께.

* **Line Type**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + True     + 8             |
+-----------------+-------+----------+---------------+

선분의 종류.

* **Shift**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + int   + True     + 0             |
+-----------------+-------+----------+---------------+

점 좌표의 소수 비트 수.

