"""
This is a high precision computing
  library based on micropython.
It can calculate functions with more than 12 digits.
'f_complex.py' is the complex-eval 
engine.
________________________________________

supported funcs:
+ - * / **(integers)
abs
pow(highacc complexs)
sin cos tan
asin acos atan
sqrt
log log10 exp


constants:
pi(chudnovsky I)
e
"""

from main import *

class cp:
    def __init__(self, arg):
        if isinstance(arg, int):
            self.re, self.im = highacc(arg), highacc('0.0')
        elif isinstance(arg, list):
            self.re, self.im = highacc(arg[0]), highacc(arg[1])
        elif isinstance(arg, highacc):
            self.re, self.im = arg, highacc(0)
        elif arg=='i' or arg=='1i' or arg=='1.0i':
            self.re, self.im = highacc(0), highacc('1.0')
        elif arg=='-i' or arg=='-1i' or arg=='-1.0i':
            self.re, self.im = highacc(0), highacc('-1.0') 
        else:
            if 'i' in arg:
                argt = arg 
                if argt[0] == '-':
                    if argt.count('-') == 1 and not('+' in arg):
                        self.re,self.im='0.0',argt 
                    else:
                        argt = argt[1:len(argt)]
                        if '+' in argt:
                            self.re,self.im=tuple(argt.split("+"))
                        elif '-' in argt:
                            self.re,self.im=tuple(argt.split("-"))
                            self.im = '-'+self.im
                        self.re = '-'+self.re 
                else:
                    if '+' in argt:
                        self.re,self.im=tuple(argt.split("+"))
                    elif '-' in argt:
                        self.re,self.im=tuple(argt.split("-"))
                        self.im = '-'+self.im
                    else:
                        self.re,self.im='0.0',argt
            else:
                self.re,self.im=arg,'0.0'
            if self.re == '':
                self.re = '0.0'
            self.re=highacc(self.re)
            if self.im=='-i':
                self.im='-1.0i' 
            if self.im=='i':
                self.im='1.0i'
            self.im=highacc(self.im[0:len(self.im)-1])
       
    def __add__(self, other):
        return cp([self.re+other.re, self.im+other.im])
        
    def __sub__(self, other):
        return cp([self.re-other.re, self.im-other.im])
             
    def __neg__(self):
        return cp([highacc('0.0')-self.re, highacc('0.0')-self.im])
             
    def __mul__(self, other):
        return cp([self.re*other.re-self.im*other.im, self.re*other.im+self.im*other.re]) 
         
    def __truediv__(self, other):
        div_=other.re*other.re+other.im*other.im
        return cp([(self.re*other.re+self.im*other.im)/div_, (self.im*other.re-self.re*other.im)/div_])
         
    def __repr__(self):
        if str(self.im)[0]=='-':
            return str(self.re)+str(self.im)+'i'
        else:
            return str(self.re)+'+'+str(self.im)+'i'
        
    def __pow__(self, other):
        return cp_pow(self, other)
"""-------------------------------------------------------------""" 

def cp_abs(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x) 
    return cp([fl_sqrt(highacc(x_.re*x_.re+x_.im*x_.im)),0])
    
     
def cp_arg(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    
    if x_.re == highacc('0.0'):
        if x_.im > highacc('0.0'):
            return cp([pi_/2,0])
        elif x_.im == highacc('0.0'):
            return cp('0.0+0.0i')
        else:
            return cp([highacc('0.0')-pi_/2,0]) 
    r=fl_atan(x_.im/x_.re)
    if x_.re<highacc('0.0') and x_.im==highacc('0.0'):
        r=pi_
    elif x_.re<highacc('0.0') and x_.im>highacc('0.0'):
        r=pi_/2-r
    elif x_.re<highacc('0.0') and x_.im<highacc('0.0'):
        r=r-pi_
    return cp([r,0])

      
def cp_log(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp([fl_log(fl_sqrt(highacc(x_.re*x_.re+x_.im*x_.im))),cp_arg(x_).re]) 
          
           
def cp_exp(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    r=fl_exp(x_.re)
    return cp([r*fl_cos(x_.im),r*fl_sin(x_.im)])
        
         
def cp_sqrt(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    if x_.re==x_.im==highacc('0.0'):
        return cp('0.0')
    return cp_exp(cp_log(x)/cp('2'))
    
     
def cp_sin(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return (cp_exp(x_*cp('i'))-cp_exp(-x_*cp('i')))/cp('2i')


def cp_cos(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return (cp_exp(x_*cp('i'))+cp_exp(-x_*cp('i')))/cp('2')

 
def cp_tan(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    a=cp_exp(x_*cp('i'))
    b=cp_exp(-x_*cp('i'))
    return cp('-i')*(a-b)/(a+b)


def cp_asin(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x) 
    return cp('-i')*cp_log(x_*cp('i')+cp_sqrt(cp('1')-x_*x_))


def cp_acos(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x) 
    return cp('-i')*cp_log(x_+cp_sqrt(x_*x_-cp('1')))


def cp_atan(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x) 
    r=(cp('i')*cp_sqrt(cp('1')+x_*x_))/(cp('i')+x_)
    if r.re==r.im==highacc('0.0'): 
        return 'inf' 
    return cp('-i')*cp_log(r)


def cp_pow(a, b):
    return cp_exp(cp_log(a)*b)

def cp_floor(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp(str(fl_floor(x_.re)))+cp('i')*cp(str(fl_floor(x_.im)))
    
     
def cp_ceil(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp(str(fl_ceil(x_.re)))+cp('i')*cp(str(fl_ceil(x_.im)))
          
  
def cp_round(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp(str(fl_round(x_.re)))+cp('i')*cp(str(fl_round(x_.im)))
    

def cp_re(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp(x_.re)
         
         
          
def cp_im(x):
    x_=x
    if not isinstance(x, cp):
        x_=cp(x)
    return cp(x_.im) 
    
     
def cp_fact(x): 
    if x.re < highacc(50):
        u = fl_floor(highacc(50) - x.re)
        t = x + cp(u)
    else:
        u = 0
        t = x 
    n = cp(u) + x + cp('0.5')
    r = cp(factConst[0]) * cp_pow(n*n/(n+cp(factConst[1])/(n+cp(factConst[2])/(n+cp(factConst[3])/(n+cp(factConst[4])/n)))),n)*cp_exp(-n) 
    for j in range(int(str(u))):
        r = r / t
        t = t - cp(1)
    return cp_round(r*cp(10**18))/cp(10**18)
    
