.. meta::
	:keywords: NUMPY

.. role:: raw-html(raw)
	:format: html

numpy_reshape
=============================

데이터를 변경하지 않고 배열에 새 형태를 적용한다.

입력 슬롯
---------

* **array**

출력 슬롯
---------

* **result**

속성 목록
---------

* **newshape**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + csv   + True     +               |
+-----------------+-------+----------+---------------+

새 형태는 원본 형태와 호환되어야 한다.

* **Order**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + False    + K             |
+-----------------+-------+----------+---------------+

Specify the memory layout of the array.

