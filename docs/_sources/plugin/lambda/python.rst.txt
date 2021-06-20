.. meta::
    :keywords: PLUGIN LAMBDA PYTHON

.. _doc-plugin-lambda-python:

람다 플러그인 Python
====================

모듈명
------

"Python Interpreter" 를 직접 실행 했을 경우 ``__main__`` 모듈로 으로 실행되는 루틴과 구분하기 위해
"엔서" 의 람다는 "Answer Python Plugin" 의 약자인 ``__app__`` 을 사용합니다.
다음과 같은 진입점을 추가할 수 있습니다.

.. code-block:: python
    :linenos:

    if __name__ == '__app__'
        pass

.. note:: 이 기능은 ``1.1.8`` 버전 부터 작동 합니다.

on_set
------

.. code-block:: python
    :linenos:

    def on_set(key, val):
        pass

속성 값을 변경 할 때 발생되는 이벤트 입니다.

on_get
------

.. code-block:: python
    :linenos:

    def on_get(key):
        return ''

속성 값을 획득 할 때 발생되는 이벤트 입니다.

on_init
-------

.. code-block:: python
    :linenos:

    def on_init():
        return True

람다가 생성된 후 초기화 할 때 호출됩니다.

반환 값이 ``True`` 가 아닐 경우 람다 초기화를 종료합니다.

on_valid
--------

.. code-block:: python
    :linenos:

    def on_valid():
        return True

람다의 정합성을 확인합니다.

반환 값이 ``True`` 가 아닐 경우 람다를 실행하지 못합니다.

on_run
------

.. code-block:: python
    :linenos:

    def on_run(array):
        return {
            "result": array[slices]
        }

람다를 실행할 구현부 입니다. (위의 예제는 ``array`` 입력과 ``result`` 출력을 갖는 람다 입니다.)

:ref:`JSON <doc-plugin-lambda-json>` 의 **controls.input** 슬롯 이름을 인자로 구현해야 합니다.

또한 :ref:`JSON <doc-plugin-lambda-json>` 의 **controls.output** 슬롯 이름을 키 값으로 ``dict`` 타입을 반환해야 합니다.

on_destroy
----------

.. code-block:: python
    :linenos:

    def on_destroy():
        pass

람다가 소멸될 때 호출됩니다.

Full example
------------

다음은 numpy slice 예제 입니다.

.. code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-

    import numpy as np

    slices = list()


    def int_or_none(val):
        return int(val) if val else None


    def str_to_slice(val):
        result = list()
        for s in str(val).split(':'):
            result.append(int_or_none(s))
        return result


    def str_to_slices(val):
        result = list()
        for s in str(val).split(','):
            result.append(str_to_slice(s))
        return result


    def slice_to_str(val):
        if len(val) == 0:
            return '::'
        elif len(val) == 1:
            return str(val[0])
        elif len(val) == 2:
            return f'{val[0]}:{val[1]}'
        elif len(val) == 3:
            return ','.join(val)
        else:
            raise IndexError('A slice must have 3 or fewer elements.')


    def slices_to_str(val):
        ','.join(list(slice_to_str(x) for x in val))


    def on_set(key, val):
        if key == 'slices':
            global slices
            slices = str_to_slices(val)


    def on_get(key):
        if key == 'slices':
            return slices_to_str(slices)


    def on_init():
        return True


    def on_valid():
        return True


    def on_run(array):
        return {
            "result": array[slices]
        }


    def on_destroy():
        pass


    if __name__ == '__app__':
        pass

