.. meta::
	:keywords: DEEP POSE HEAD

.. role:: raw-html(raw)
	:format: html

head_pose_detect
=============================

.

입력 슬롯
---------

* **image**

출력 슬롯
---------

* **draw_image**

* **heads**

속성 목록
---------

* **Weights 파일 1 경로**

+-----------------+-------+----------+-----------------------------------------------+
| Rule            + Type  + Required + Default value                                 |
+=================+=======+==========+===============================================+
| read_and_write  + str   + True     + head_pose_fsanet/fsanet_capsule_3_16_2_21_5.h5|
+-----------------+-------+----------+-----------------------------------------------+



* **Weights 파일 2 경로**

+-----------------+-------+----------+---------------------------------------------------+
| Rule            + Type  + Required + Default value                                     |
+=================+=======+==========+===================================================+
| read_and_write  + str   + True     + head_pose_fsanet/fsanet_var_capsule_3_16_2_21_5.h5|
+-----------------+-------+----------+---------------------------------------------------+



* **Weights 파일 3 경로**

+-----------------+-------+----------+----------------------------------------------------+
| Rule            + Type  + Required + Default value                                      |
+=================+=======+==========+====================================================+
| read_and_write  + str   + True     + head_pose_fsanet/fsanet_noS_capsule_3_16_2_192_5.h5|
+-----------------+-------+----------+----------------------------------------------------+



* **Face Proto 파일 경로**

+-----------------+-------+----------+---------------------------------+
| Rule            + Type  + Required + Default value                   |
+=================+=======+==========+=================================+
| read_and_write  + str   + True     + head_pose_fsanet/deploy.prototxt|
+-----------------+-------+----------+---------------------------------+



* **Face Weights 파일 경로**

+-----------------+-------+----------+----------------------------------------------------------+
| Rule            + Type  + Required + Default value                                            |
+=================+=======+==========+==========================================================+
| read_and_write  + str   + True     + head_pose_fsanet/res10_300x300_ssd_iter_140000.caffemodel|
+-----------------+-------+----------+----------------------------------------------------------+



* **이미지 전달 여부**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + True     + True          |
+-----------------+-------+----------+---------------+



