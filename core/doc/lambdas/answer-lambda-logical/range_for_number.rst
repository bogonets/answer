.. meta::
	:keywords: NUMBER

.. role:: raw-html(raw)
	:format: html

range_for_number
=============================



입력 슬롯
---------

* **number**

출력 슬롯
---------

* **result**

속성 목록
---------

* **결과 반전**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + True     + False         |
+-----------------+-------+----------+---------------+



* **데이터 전달 차단 여부**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + True     + False         |
+-----------------+-------+----------+---------------+

'number'가 None 이거나 범위에 들어오지 않을때, 데이터 전달을 차단한다.

* **시작 범위**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + float + True     + 0.0           |
+-----------------+-------+----------+---------------+

start <= x

* **시작 범위 지정 여부**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + True     + True          |
+-----------------+-------+----------+---------------+

 ~ x

* **끝 범위**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + float + True     + 0.0           |
+-----------------+-------+----------+---------------+

x <= end

* **끝 범위 지정 여부**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + True     + True          |
+-----------------+-------+----------+---------------+

x ~ 

