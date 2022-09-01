.. meta::
	:keywords: NUMPY

.. role:: raw-html(raw)
	:format: html

numpy_array
=============================

배열을 생성한다.

출력 슬롯
---------

* **result**

속성 목록
---------

* **Elements**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + csv   + True     +               |
+-----------------+-------+----------+---------------+

List of all elements.

* **shape**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + csv   + True     +               |
+-----------------+-------+----------+---------------+

Shape of the new array.

* **dtype**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + True     + int32         |
+-----------------+-------+----------+---------------+

Numpy dtype.

* **Order**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + str   + False    + K             |
+-----------------+-------+----------+---------------+

Specify the memory layout of the array.

* **Subok**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + bool  + False    + True          |
+-----------------+-------+----------+---------------+

If True, then sub-classes will be passed-through.

* **ndmin**

+-----------------+-------+----------+---------------+
| Rule            + Type  + Required + Default value |
+=================+=======+==========+===============+
| read_and_write  + int   + False    + 0             |
+-----------------+-------+----------+---------------+

Specifies the minimum number of dimensions that the resulting array should have.

