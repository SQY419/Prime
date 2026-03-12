## python程序
一般使用python和ppl混合编写. ppl是什么？ `Prime Programming Language`，HP Prime自带的编程语言.
HP Prime自带`micropython 1.9.4`.

python与ppl
python中引用ppl代码如下：
```python
from hpprime import eval as ppleval

print(ppleval('print("hello ppl!")'))
```
若要引用hpprime中的其他内容，只需要：
```python
from hpprime import *
from hpprime import eval as ppleval

print(ppleval('print("hello ppl!")'))
```
