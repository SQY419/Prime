"""
This is a high precision computing library based on micropython.
It can calculate different kinds of  functions with more than 12 digits.
'main.py' is the real-eval engine.
The complex engine uses this program.
Besides, using this program and 'gauss-kronrod' can make a high precision integrate calculator.
  
________________________________________

supported funcs:
+ - * / **(integers)
abs
agm
pow(highacc floats)
sin cos tan
asin acos atan
sinh cosh tanh
log log10 exp
sqrt
floor ceil round
fact(ℝ)
ipmod

constants:
pi(chudnovsky I)
e
"""

 
from math import *
from math import pi as p_t
from math import e as e_t


class highacc: 
    prec = 80
    a = 10 ** prec
    def __init__(self, arg):
        if isinstance(arg, int):
            self.val = arg * highacc.a
        elif isinstance(arg, list):
            self.val = arg[0]
        elif arg in ['inf', '-inf', 'undef']:
            self.val = arg
        else:
            if type(arg) != highacc:
                if arg == '.':
                    intp, frcp = '0', '0' 
                else:
                    if '.' in arg:
                        intp, frcp = tuple(arg.split("."))
                    else:
                        intp, frcp = tuple((arg+'.0').split("."))
            else:
                a_ = str(arg)
                if a_.find('.') == -1:
                    intp, frcp = a_, '0'
                else: 
                    intp, frcp = tuple(a_.split(".")) 
            frcp = int((frcp + "0" * highacc.prec)[:highacc.prec])
            if intp[0] == '-':
                self.val = int(intp) * highacc.a - frcp
            else:
                self.val = int(intp) * highacc.a + frcp
    """-------------------------------------------------------"""
    def __add__(self, other):
        if self.val == 'undef' or other == highacc('undef'):
            return highacc('undef')
        elif self == highacc('inf'):
            if other.val == '-inf':
                return highacc('undef')
            else:
                return highacc('inf')
        elif self == highacc('-inf'):
            if other.val == 'inf':
                return highacc('undef')
            else:
                return highacc('-inf') 
        elif other == highacc('inf'):
            if self == highacc('-inf'):
                return highacc('undef')
            else:
                return highacc('inf') 
        elif isinstance(other, int):
            return highacc([other * highacc.a + self.val])
        elif isinstance(other, highacc):
            return highacc([other.val + self.val])
    def __radd__(self, other):
        if self.val == 'undef':
            return highacc('undef')
        elif self == highacc('inf'):
            if other == highacc('-inf'):
                return highacc('undef')
            else:
                return highacc('inf') 
        elif isinstance(other, int):
            return highacc([other * highacc.a + self.val])
        elif isinstance(other, highacc):
            return highacc([other.val + self.val])
    """-------------------------------------------------------"""
    def __sub__(self, other):
        if self.val == 'undef':
            return highacc('undef')
        elif self == highacc('inf'):
            if other.val == '-inf':
                return highacc('inf')
            else:
                return highacc('undef')
        elif self == highacc('-inf'):
            if other.val == '-inf':
                return highacc('undef')
            else:
                return highacc('-inf')
        elif other == highacc('inf'):
            return highacc('-inf') 
        elif isinstance(other, int):
            return highacc([self.val - other * highacc.a])
        elif isinstance(other, highacc):
            return highacc([self.val - other.val])
    def __neg__(self): 
        if self.val == 'undef':
            return highacc('undef')
        elif self.val == 'inf':
            return highacc('-inf')
        elif self.val == '-inf':
            return highacc('inf')
        return highacc([0 - self.val])
   
    """-------------------------------------------------------"""
    def __mul__(self, other):
        if self.val == 'undef':
            return highacc('undef')
        elif isinstance(other, int):
            return highacc([self.val * other])
        elif isinstance(other, highacc):
            return highacc([(self.val * other.val) // highacc.a])
    """-------------------------------------------------------"""
    def __truediv__(self, other):
        if self.val == 'undef':
            return highacc('undef')
        elif isinstance(other, int):
            return highacc([self.val // other])
        elif isinstance(other, highacc):
            if self == highacc('inf') or self == highacc('-inf'):
                if other == highacc('inf') or other == highacc('-inf'):
                    return highacc('undef')
                else:
                    return self 
            if other.val == 0:
                if self.val < 0: 
                    return highacc('-inf')
                elif self.val > 0: 
                    return highacc('inf')
                elif self.val == 0: 
                    return highacc('undef')
            elif other == highacc('inf') or other == highacc('-inf'):
                return highacc('0.0') 
            else: 
                return highacc([(self.val * highacc.a) // other.val])
                
    def __floordiv__(self, other):
        return fl_floor(self / other)
        
    def __mod__(self, other):
        if isinstance(self, highacc):
            s = self
        else:
            s = highacc(self)
        if isinstance(other, highacc):
            o = other
        else:
            o = highacc(other) 
        return s - o * (s // o)
    """-------------------------------------------------------"""
    def __repr__(self):
        if self.val == 'inf' or self.val == '-inf' or self.val == 'undef':
            return self.val 
        elif self.val >= 0:
            frcp = str(self.val % highacc.a)
            frcp = ("0" * highacc.prec + frcp)[-highacc.prec:]
            intp = str(self.val // highacc.a)
            while frcp[-1] == "0" and frcp != "0":
                frcp = frcp[:-1]
            if frcp == "0":
                return intp
            else: 
                return intp + "." + frcp
        else:
            frcp = str(-self.val % highacc.a)
            frcp = ("0" * highacc.prec + frcp)[-highacc.prec:]
            intp = str(-self.val // highacc.a)
            while frcp[-1] == "0" and frcp != "0":
                frcp = frcp[:-1]
            if frcp == "0":
                return '-' + intp
            else:
                return '-' + intp + "." + frcp 
    """-----------------------------------------------------------"""
    def __pow__(self, other):
        if isinstance(other,int):
            if other == 1:
                return highacc([self.val])
            elif other & 1:
                b = (self ** (other >> 1)) 
                return b * b * self
            else:
                b = (self ** (other >> 1))
                return b * b
        else:
            return fl_pow(self, other)
    """-----------------------------------------------------------"""
    def __eq__(self,other):
        if isinstance(other,int):
            return other * highacc.a == self.val
        else:
            return other.val == self.val 
    def __gt__(self,other):
        if isinstance(other,int):
            return other * highacc.a < self.val
        else:
            return other.val < self.val
    def __ge__(self, other):
        if isinstance(other, int):
            return other * highacc.a < self.val
        else:
            return other.val < self.val
    def __lt__(self, other):
        if other == highacc('inf'):
            if self != highacc('inf'):
                return True
            else:
                return False
        if self == highacc('-inf'):
            if other != highacc('-inf'):
                return True
            else:
                return False
        if isinstance(other,int):
            return other * highacc.a > self.val
        else:
            return other.val > self.val
    def __le__(self, other):
        if isinstance(other,int):
            return other * highacc.a > self.val
        else:
            return other.val > self.val
"""-----------------------------------------------------------"""


def bs(a,b):
    if b-a==1:
        if a==0:
            Pab=Qab=1
        else:
            Pab=(6*a-5)*(2*a-1)*(6*a-1)
            Qab=a*a*a*10939058860032000
        Tab=Pab*(13591409+545140134*a)
        if a&1:
            Tab=-Tab
    else:
        m=(a+b)//2
        Pam,Qam,Tam=bs(a,m)
        Pmb,Qmb,Tmb=bs(m,b)
        Pab=Pam*Pmb
        Qab=Qam*Qmb
        Tab=Qmb*Tam+Pam*Tmb
    return Pab,Qab,Tab
       
        
def chud_pi(w):
    if w<=100:
        r='31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170657'
        return '3.'+r[1:w+1] 
    wp=w
    p=10**(wp*2)
    
    #isqrt10005
    
    s10005=10002*10**(wp-2)
    a=0
    t=1
    while t>0:
        s10005=(s10005+10005*10**(wp*2)//s10005)//2
        t=abs(s10005-a)
        a=s10005
    
    P,Q,T=bs(0,int(w/14.81)+1)
    r=str(Q*426880*s10005//T)
    return '3.'+r[1:len(r)]


def fl_e(w):
    if w<=100:
        r='27182818284590452353602874713526624977572470936999595749669676277240766303535475945713815114073671093'
        return '2.'+r[1:w+1] 
    else:
        return fl_exp('1.0') 


"""------Const ___init___ --------------------------"""

def fl_is_inf(x):
    if type(x)==highacc:
        return str(x) in ['inf', '-inf', 'undef'] 
    else:
        return x in ['inf', '-inf', 'undef'] 


def fact(x):
    #simple integer factorial
    if x<0 :
        return 'undef'
    if x==0:
        return 1
    i=j=1
    while i<=x:
        j*=i
        i+=1
    return j


def fl_sin(x):
    if fl_is_inf(x):
        return highacc('undef')
    x0_=str(x)
    if '-' in x0_:
        return -fl_sin(-highacc(x))
    digi=len(x0_)
    if '.' in x0_:
        digi=x0_.find('.')
    d=floor((digi-1)/0.47712125472)+32
    setprec(highacc.prec+30)
    x_=highacc(x0_) / 3 ** d
    u_=x_ ** 2
    i=0 
    f=1
    sum=highacc('0.0')
    while i<=(highacc.prec/15.26):
        se_=x_ / fact(2*i+1)
        if f==1:
            sum=sum + se_
        else:
            sum=sum - se_
        x_=x_ * u_
        i+=1
        f*=-1
    for i in range(d):
        sum = highacc('3.0') * sum - highacc('4.0') * sum ** 3
    setprec(highacc.prec-30)
    return sum / 10 ** 30
         
          
def fl_cos(x):
    if fl_is_inf(x):
        return highacc('undef')
    t=fl_sin(x / 2)
    return highacc('1.0') - t * t * 2
    
     
def fl_tan(x):
    if fl_is_inf(x):
        return highacc('undef')
    return fl_sin(x)/fl_cos(x)
    
     
def fl_exp(x):
    x0_=str(x)
    if x0_ == 'inf':
        return highacc('inf')
    elif x0_ == '-inf':
        return highacc('0.0')
    elif x0_ == 'undef':
        return highacc('undef')
    digi=len(x0_)
    if '.' in x0_:
        digi=x0_.find('.')
    d=floor((digi-1)/0.30102999564)+40
    setprec(highacc.prec+30)
    x_=highacc(x0_) / 2 ** d
    u_=x_
    i=1
    sum=highacc('1.0')
    while i<=highacc.prec/12.04+3:
        sum=sum + x_ / fact(i)
        x_=x_ * u_
        i+=1
    for i in range(d):
        sum = sum * sum
    setprec(highacc.prec-30)
    return sum/10**30
    

def fl_sqrt(x):
    x_ = str(x)
    if x_ == '0.0' or x_ == '0':
        return highacc('0.0')
    elif float(x_) < 0.0:
        return 'undef' 
    elif x_ == 'inf':
        return highacc('inf') 
    if '.' in x_:
        digi=x_.find('.')
    else:
        digi=len(x_) 
    r=highacc(10**(digi//2))
    a=r
    t=highacc('1.0')
    hx=highacc(x_)
    while fl_abs(t) > highacc('1.0')/10**highacc.prec:
        r=highacc('0.5')*(r+hx/r)
        t=r-a
        a=r
    return r

 
def fl_log10_const():
    x0=highacc('10')/e_**2
    x_=(x0-highacc('1.0'))/(x0+highacc('1.0'))
    i=0
    s=highacc('0.0')
    while i<=highacc.prec/1.8+2:
        s+=x_**(2*i+1)/(2*i+1)
        i+=1
    s*=2
    s=s-1+x0/fl_exp(s)
    return s+2


def fl_log10(x):
    if x == 'undef' or x == highacc('undef'):
        return highacc('undef')
    if isinstance(x, highacc):
        x0=x
    else:
        x0=highacc(x)
    if x0 == highacc('0.0'):
        return highacc('-inf')
    elif x0 == highacc('1.0'):
        return highacc('0.0')
    elif x0 == highacc('inf'):
        return x0 
    elif x0<0:
        return highacc('undef')
    return fl_log(x)/ln10_


def fl_pow(a,b):
    t=str(b) 
    if float(t) > 10**20:
        return highacc('undef')
    if '-' in t:
        return highacc('1.0')/fl_pow(a, -b) 
    if t == '1' or t=='1.0':
        return a
    if t == '0' or t=='0.0':
        if str(a) == '0':
            return highacc('undef')
        return highacc('1')
    else:
        if t.find('.') != -1:
            return fl_exp(fl_log(a)*b)
        else:
            if int(t) % 2==1:
                u = fl_pow(a,int(t)//2)
                return u * u * a
            else:
                u = fl_pow(a,int(t)//2)
                return u * u 

 
def fl_intpowmod(a,b,c): 
    if b == 1:
        return a % c
    elif b % 2 == 1:
        return (fl_intpowmod(a, b//2, c) ** 2 * a) % c
    elif b % 2 == 0:
        return fl_intpowmod(a, b//2, c) ** 2 % c


def fl_ipmod(a,b,c):
    a_=str(a)
    if '.' in a_ or '-' in a_:
        return highacc('undef')
    a_=int(a_)
    b_=str(b)
    if '.' in b_ or '-' in b_:
        return highacc('undef')
    b_=int(b_)
    if b_ > 10**20:
        return highacc('undef')
    c_=str(c)
    if '.' in c_ or '-' in c_:
        return highacc('undef')
    c_=int(c_)
    return highacc(fl_intpowmod(a_, b_, c_))
   

def fl_log(x):
    if x == 'undef' or x == highacc('undef'):
        return highacc('undef')
    if isinstance(x, highacc):
        x0=x
    else:
        x0=highacc(x)
    if x0 == highacc('0.0'):
        return highacc('-inf')
    elif x0==highacc('1.0'):
        return highacc('0.0')
    elif x0 == highacc('inf'):
        return x0
    elif x0<0:
        return highacc('undef')
    elif x0<highacc('1.0'):
        return highacc('0.0')-fl_log(highacc('1.0')/x0) 
    x_=str(x)
    digi=len(x_)
    if '.' in x_:
        digi=x_.find('.')
    base10=digi-1
    x0=x0/10**(base10)
    base=highacc('0.0')
    while '-' in str(e_-x0):
        x0=x0/e_
        base+=1
    x_=(x0-highacc('1.0'))/(x0+highacc('1.0'))
    i=0
    s=highacc('0.0')
    while i<=highacc.prec/1.8+2:
        s+=x_**(2*i+1)/(2*i+1)
        i+=1
    s*=2
    s=s-1+x0/fl_exp(s)
    return s+base+ln10_*base10
  
   
def setprec(w): 
    highacc.prec = w
    if w<10:
        highacc.prec = 10
    if w>5000:
        highacc.prec = 5000
    highacc.a = 10**highacc.prec 
    


def fl_abs(x):
    if x == 'undef' or x == highacc('undef'):
        return highacc('undef')
    elif fl_is_inf(x):
        return highacc('inf')
    if type(x) == highacc:
        x0 = x
    else:
        x0 = highacc(x) 
    if x0 < highacc('0.0'):
        return -x0
    else:
        return x0
  

def fl_atan(x):
    if str(x) in ['0', '0.', '0.0']:
        return highacc('0.0')
    elif str(x)=='inf':
        return pi_/2
    elif str(x)=='-inf':
        return -pi_/2 
    setprec(highacc.prec+20) 
    if type(x)==highacc:
        x0=x*10**20
    else:
        x0=highacc(x)
    if x0<highacc('0.0'):
        inv=-1
        x0=highacc('0.0')-x0
    else:
        inv=1
    if x0 > highacc('1.0'):
        x0 = highacc('1.0')/x0
        pinv=1 
    else:
        pinv=0
    if x0 == highacc(0):
        sum = r = highacc(0)
    else:
        x0 = (fl_sqrt(x0**2+1)-1)/x0
        base=1
        while float(str(x0-highacc('0.001')))>0:
            x0=(fl_sqrt(x0**2+1)-1)/x0
            base+=1
        x_=x0
        u_=x0*x0
        i=0
        f=1
        sum=highacc('0.0')
        while i<=highacc.prec/8+4:
            if f==1: 
                sum=sum + x_ / (2*i+1)
            else: 
                sum=sum - x_ / (2*i+1)
            x_=x_ * u_
            i+=1
            f*=-1
        r=highacc('2.0') ** base * sum
    setprec(highacc.prec-20)
    r=r/10**20
    if pinv:
        r=pi_/2-r
    if inv==-1:
        r=-r
    return r


def fl_asin(x):
    if type(x)==highacc:
        x0=x
    else:
        x0=highacc(x)
    if x0==highacc('1.0'):
        return pi/2
    elif x0==highacc('-1.0'):
        return -pi/2 
    t=highacc('1.0')-x0**2
    if t < highacc('0.0'): 
        return highacc('undef')
    else: 
        r=x0/fl_sqrt(t)
    r=fl_atan(r)
    return r
    

def fl_acos(x):
    if fl_abs(x) > highacc('1.0'): 
        return highacc('undef')
    else: 
        return pi_/2-fl_asin(x)


def fl_agm(a,b):
    a1=highacc(a)
    b1=highacc(b)
    while fl_abs(a1-b1) != highacc('0.0'):
        a2=highacc('0.5')*(a1+b1)
        b2=fl_sqrt(a1*b1)
        a1=a2
        b1=b2 
    return a1;


def fl_sinh(x):
    if fl_is_inf(x):
        return x
    sinh_temp = fl_exp(x)
    return (sinh_temp - highacc('1.0') / sinh_temp) / 2 
    

def fl_cosh(x):
    if fl_is_inf(x):
        return fl_abs(x)
    cosh_temp = fl_exp(x)
    return (cosh_temp + highacc('1.0') / cosh_temp) / 2 
    
     
def fl_tanh(x):
    if x in ['inf', highacc('inf')]:
        return highacc('1.0')
    elif x in ['-inf', highacc('-inf')]:
        return highacc('-1.0')
    elif x in ['undef', highacc('undef')]:
        return highacc('undef')
    cosh_temp = fl_exp(x)
    return (cosh_temp - highacc('1.0') / cosh_temp) / (cosh_temp + highacc('1.0') / cosh_temp) 


def fl_floor(x):
    fl_t = str(x)
    if '.' in fl_t:
        if int(fl_t[fl_t.find('.')+1:]) == 0:
            return highacc(fl_t[:fl_t.find('.')])
        fl_t1 = fl_t[:fl_t.find('.')]
        if fl_t.find('-') == 0:
            fl_t1 = highacc(fl_t1) - highacc('1.0') 
        else:
            fl_t1 = highacc(fl_t1)
        return fl_t1
    else:
        if isinstance(x, highacc):
            return x
        else:
            return highacc(x)
        

def fl_ceil(x):
    fl_t = str(x)
    if '.' in fl_t:
        if int(fl_t[fl_t.find('.')+1:]) == 0:
            return highacc(fl_t[:fl_t.find('.')])
        fl_t1 = fl_t[:fl_t.find('.')]
        if fl_t.find('-') != 0:
            fl_t1 = highacc(fl_t1) + highacc('1.0') 
        else:
            fl_t1 = highacc(fl_t1)
        return fl_t1
    else:
        if isinstance(x, highacc):
            return x
        else:
            return highacc(x)
  

def fl_round(x):
    return fl_floor(highacc('0.5')+x)
 

def fl_fact(x):
    if str(x).find('.') == -1:
        if x == highacc('inf'):
            return x
        elif x == highacc('-inf') or x == highacc('undef'):
            return highacc('undef') 
        return highacc(fact(int(str(x))))
    if x < highacc(60):
        u=fl_floor(highacc(60) - x)
        t=x+u
    else:
        u=0
        t=x
    n = u + x + highacc('0.5')
    r = factConst[0] * fl_pow(n*n/(n+factConst[1]/(n+factConst[2]/(n+factConst[3]/(n+factConst[4]/n)))),n)*fl_exp(-n) 
    for j in range(int(str(u))):
        r = r / t
        t = t - highacc(1)
    return fl_round(r*10**15)/10**15
    


pi_=highacc(chud_pi(highacc.prec))
e_=highacc(fl_e(highacc.prec))
ln10_=fl_log10_const()

factConst=[fl_sqrt(pi_*highacc('2.0')), highacc(1)/highacc(24), highacc('0.0375'), highacc(18029)/highacc(45360), highacc(6272051)/highacc(14869008)]

pi=π=pi_
e=e_
