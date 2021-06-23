.. meta::
	:keywords: CV2 MATCH FILTER

.. role:: raw-html(raw)
	:format: html

cv2_match_distance_filter
=============================

Match 결과의 Distance 필터

입력 슬롯
---------

* **query**

* **train**

출력 슬롯
---------

* **good**

속성 목록
---------

* **ratio**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + float + True     + 0.7           |
+-----------------+-------+----------+---------------+

(query < train*ratio)

