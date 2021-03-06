.. meta::
	:keywords: CV2

.. role:: raw-html(raw)
	:format: html

cv2_polylines
=============================

다각형을 그린다.

입력 슬롯
---------

* **source**

* **points**

출력 슬롯
---------

* **result**

속성 목록
---------

* **Polylines color**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + color + True     + #000000       |
+-----------------+-------+----------+---------------+

다각형을 구성하는 선의 색.

* **Line thickness**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + int   + True     + 1             |
+-----------------+-------+----------+---------------+

다각형을 구성하는 선분의 두께. 각형의 내부를 채우고싶다면 음수를 전달하면 된다.

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

* **Is Closed**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + True     + True          |
+-----------------+-------+----------+---------------+

그려진 폴리라인이 닫혔는지 여부 (True = 닫힌 도형, False = 열린 도형).

