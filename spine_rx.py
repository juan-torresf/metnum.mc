import re,numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
from sympy import symbols,sin,cos,lambdify,diff,latex,sympify,simplify

_,ax = plt.subplots()
ax.imshow(mpimg.imread(r'spine.jpg'),extent=[-210,247,-94,95],alpha=.8)

x = symbols('x')
f = 3*(sin((1/80)*x)-(1/100)*x)-4*(2*cos((1/30)*x)+5)
fx = lambdify(x,f,'numpy')
dfx = lambdify(x,diff(f,x),'numpy')

points = [(x,fx(x))for x in np.linspace(-115,133,19)]

def frac_latex(match):
    if(Fraction(float(match.group())).limit_denominator(10000).denominator==1):
        return str(Fraction(float(match.group())).limit_denominator(10000).numerator)
    else:
        return f'\\frac{{{Fraction(float(match.group())).limit_denominator(10000).numerator}}}{{{Fraction(float(match.group())).limit_denominator(10000).denominator}}}'

f = re.sub(r'\b0\.\d+\b',frac_latex,latex(f,mode='inline',fold_short_frac=False))

plt.plot(np.linspace(-115,133,400),fx(np.linspace(-115,133,400)),linestyle='solid',linewidth=2,label=fr'f(x) = {f}',color='white')

for (x_,y_),color in zip(points,plt.cm.rainbow(np.linspace(0,1,len(points)))):
    ax.scatter(x_,y_,color=color,s=50)

ax.axhline(y=0,color='black',linewidth=1)
ax.axvline(x=0,color='black',linewidth=1)
ax.set_xlim(-210,247)
ax.set_ylim(-94,95)
ax.set_xlabel('x')
ax.set_ylabel('f(x)',rotation=0,labelpad=0)
ax.grid(True,linestyle='--',alpha=.5)

flegend = ax.legend(title=fr'función',loc='upper left')
ax.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=color,markersize=8,label=f'({int(x)},{int(y)})')for(x,y),color in zip(points,plt.cm.rainbow(np.linspace(0,1,len(points))))],title='puntos',loc='upper right')
ax.add_artist(flegend)

plt.show()
