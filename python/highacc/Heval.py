from main import *
from f_complex import *
import hpprime

def hprint(text):
  if len(text) <= 52:
    hpprime.eval('print2d("'+text+'",0)\n')
  else:
    for i in range(len(text) // 52):
      hpprime.eval('print2d("'+text[i*52:i*52+52]+'",0)\n')
    hpprime.eval('print2d("'+text[i*52+52:]+'",0)\n')
      

print = hprint

def reset(m):
  global arg,re,im,sin,cos,tan,sinh,cosh,tanh,asin,acos,atan,log,log10,ln,sqrt,abs,floor,ceil,round,fact,exp,ipmod 
  if m == 0:
    log10=fl_log10
    sin=fl_sin
    cos=fl_cos
    tan=fl_tan
    sinh=fl_sinh
    cosh=fl_cosh
    tanh=fl_tanh
    asin=fl_asin
    acos=fl_acos
    atan=fl_atan
    sqrt=fl_sqrt
    abs=fl_abs
    exp=fl_exp
    ln=fl_log
    floor=fl_floor
    ceil=fl_ceil
    round=fl_round
    ipmod=fl_ipmod
    fact=fl_fact
  else:
    log10=fl_log10
    sin=cp_sin
    cos=cp_cos
    tan=cp_tan
    sinh=fl_sinh
    cosh=fl_cosh
    tanh=fl_tanh
    asin=cp_asin
    acos=cp_acos
    atan=cp_atan
    sqrt=cp_sqrt
    abs=cp_abs
    exp=cp_exp
    ln=cp_log
    floor=cp_floor
    ceil=cp_ceil
    round=cp_round
    re=cp_re
    im=cp_im
    fact=cp_fact
    arg=cp_arg
   


op=['+', '-', '*', '/', '^', '(', ')', ',', "'", '[', ']', '{', '}']


def sp(expr):
  e_stack=[]
  temp=''
  for i in range(len(expr)):
    if expr[i] in op:
      if temp != '':
        e_stack.append(temp)
      e_stack.append(expr[i])
      temp=''
    else:
      temp+=expr[i]
  if temp != '':
    e_stack.append(temp) 
  return e_stack 
 
  
def fSolve(fun, x0):
  x=x0
  feq = eval('lambda X: '+fun)
  for i in range(9):
    dx=highacc('1') / highacc(10) ** (highacc.prec//4)
    y0=feq(x + dx) 
    y1=feq(x - dx) 
    x=x-feq(x)*dx*2/(y0-y1)
  return x
  
def turnIntoHa(s):
  e_stack=s
  for i in range(len(e_stack)):
    try: 
      a=float(e_stack[i])
      b='num'
    except ValueError:
      if (e_stack[i])[-1]=='i':
        a=e_stack[i]
        b='num'
      else: 
        a=e_stack[i]
        b='str'
    if b=='num':
      if mode==0:
        e_stack[i]="highacc('"+e_stack[i]+"')"
      else:
        e_stack[i]="cp('"+e_stack[i]+"')"
    elif e_stack[i]=='^':
      e_stack[i]='**'
    elif e_stack[i]=='oo':
      e_stack[i]="highacc('inf')"
  u=''
  for i in range(len(e_stack)):
    u+=e_stack[i]
  return u
 
hpprime.eval("print;")
for i in range(8): print('')


initp = [
'            Prime High Precision Library ',
'            PHPL v0.1.0',
'',
"            type 'quit' to quit PHPL...",
"            type 'oN' to use the N th result",
"            type 'cpm' to use complex mode",
"            type 'rem' to use real mode","","",
'            Default prec: '+str(highacc.prec),
"",
]
for i in initp:
  print(i)
co=0
mode=0
reset(0)


def uni(iexpr):
  global co, mode
  if iexpr=='':
    print('In['+str(co)+']:= (empty)')
    print('Out['+str(co)+']= ?')
  elif iexpr=='cpm':
    print('Complex Mode...')
    mode=1
    reset(1)
  elif iexpr=='rem':
    print('Real Mode...')
    mode=0
    reset(0)
  else: 
    print('In['+str(co)+']:= '+iexpr)
    try:
      k = turnIntoHa(sp(iexpr))
      f = eval('lambda X: '+k)
      r = str(f(0))
      if mode == 0:
        exec('o'+str(co)+"=highacc('"+r+"')")
      else:
        exec('o'+str(co)+"=cp('"+r+"')")
      print('Out['+str(co)+']= '+r)
    except Exception as e:
      print('Out['+str(co)+']: PHPL Error, '+str(e)) 
    print("")
  co+=1
  

while True:
  try:
    iexpr=input()
    if iexpr == "exit":
      print("")
      break
    uni(iexpr)
  except KeyboardInterrupt:
    print("")
    break
    