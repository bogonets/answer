.. meta::
	:keywords: DEEP DETECTRON2 MASKRCNN FASTER-RCNN

.. role:: raw-html(raw)
	:format: html

detectron2_filter_by_class
=============================

클래스로 필터링 한다.

입력 슬롯
---------

* **bboxes**

출력 슬롯
---------

* **filtered_bboxes**

* **remain**

속성 목록
---------

* **필터 조건**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + list  + True     +               |
+-----------------+-------+----------+---------------+

원하는 객체를 선택한다.

* **names 파일**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + True     +               |
+-----------------+-------+----------+---------------+



