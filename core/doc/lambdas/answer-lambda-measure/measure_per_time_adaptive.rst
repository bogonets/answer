.. meta::
	:keywords: MEASURE

.. role:: raw-html(raw)
	:format: html

measure_per_time_adaptive
=============================

입력이 일정 단위 동안 들어오는지 측정한다.

입력 슬롯
---------

* **array**

* **fps**

출력 슬롯
---------

* **result**

* **labels**

속성 목록
---------

* **기준 초**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + list  + True     + 1             |
+-----------------+-------+----------+---------------+



* **측정 라벨**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + list  + True     + Occur1        |
+-----------------+-------+----------+---------------+



* **기준 초 동안 입력 비율**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + list  + True     + 0.5           |
+-----------------+-------+----------+---------------+



* **결과 출력 주기(초)**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + list  + True     + 1             |
+-----------------+-------+----------+---------------+



