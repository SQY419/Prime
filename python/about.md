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


## 这个文件夹下有什么？
 - HighAcc.hpappdir: 使用mpy编写而成的高精度计算库，支持实数和复数的高精度计算。

  <img width="584" height="480" alt="image" src="https://github.com/user-attachments/assets/2a4397c6-b827-4c3d-93e8-865db19fd77d" />

 - PrimeCode：使用mpy编写而成的机上代码编辑器，保证实体机（C版）可用。字符等宽，自动高亮，提示，查找和替换均支持。

![](https://github.com/SQY419/Prime/blob/main/src/000.jpg)

## 如何使用？
将zip文件解压得到***.hpappdir，使用HP Connectivity Kit将整个文件夹传入你的计算器。
