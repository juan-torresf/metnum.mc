from os import name,system
from spine_rx import np,points,x,dfx as df,sympify,simplify,lambdify,plt,mpimg

def natural(points=points):

    h,alpha= [0]*(len(points)),[0]*(len(points))
    l,u,z = [0]*(len(points)+1),[0]*(len(points)+1),[0]*(len(points)+1)
    a,b,c,d = [0]*(len(points)),[0]*(len(points)),[0]*(len(points)+1),[0]*(len(points))

    h[1:] = [points[i][0]-points[i-1][0]for i in range(1,len(points))]
    alpha[1:len(points)-1] = [3*((points[i+1][1]-points[i][1])/h[i+1]-(points[i][1]-points[i-1][1])/h[i]) for i in range(1,len(points)-1)]

    l[1],u[1],z[1] = 1,0,0
    for i in range(2,len(points)):
        l[i] = 2*(points[i][0]-points[i-2][0])-h[i-1]*u[i-1]
        u[i] = h[i]/l[i]
        z[i] = (alpha[i-1]-h[i-1]*z[i-1])/l[i]

    c[len(points)] = 0
    for i in range(len(points)-1, 0, -1):
        c[i] = z[i]-u[i]*c[i+1]
        b[i] = (points[i][1]-points[i-1][1])/h[i]-h[i]*(c[i+1]+2*c[i])/3
        d[i] = (c[i+1]-c[i])/(3*h[i])
        a[i] = points[i-1][1]

    return [a[1:],b[1:],c[1:len(points)],d[1:]]

def sujeto(points=points,df=df):
    
    h,alpha = [0]*(len(points)),[0]*(len(points))
    l,u,z = [0]*(len(points)+1),[0]*(len(points)+1),[0]*(len(points)+1)
    a,b,c,d = [0]*(len(points)),[0]*(len(points)),[0]*(len(points)+1),[0]*(len(points))
    
    h = [0]+[points[i][0]-points[i-1][0]for i in range(1,len(points))]
    
    alpha[0] = 3*((points[1][1]-points[0][1])/h[1]-df(points[0][0]))
    alpha[len(points)-1] = 3*(df(points[len(points)-1][0])-(points[len(points)-1][1]-points[len(points)-1-1][1])/h[len(points)-1])
    for i in range(1,len(points)-1):
        alpha[i] = 3*((points[i+1][1]-points[i][1])/h[i+1]-(points[i][1]-points[i-1][1])/h[i])
    
    l[1],u[1],z[1] = 2*h[1],1/2,alpha[0]/2*h[1]
    for i in range(2,len(points)):
        l[i] = 2*(points[i][0]-points[i-2][0])-h[i-1]*u[i-1]
        u[i] = h[i]/l[i]
        z[i] = (alpha[i-1]-h[i-1]*z[i-1])/l[i]

    c[len(points)] = (alpha[len(points)-1]-h[len(points)-1]*z[len(points)-1])/(h[len(points)-1]*(2-u[len(points)-1]))
    for i in range(len(points)-1,0,-1):
        c[i] = z[i]-u[i]*c[i+1]
        b[i] = (points[i][1]-points[i-1][1])/h[i]-h[i]*(c[i+1]+2*c[i])/3
        d[i] = (c[i+1]-c[i])/(3*h[i])
        a[i] = points[i-1][1]

    return a[1:], b[1:], c[1:len(points)], d[1:]

def splines(trazadores):

    _,pt = plt.subplots()
    pt.imshow(mpimg.imread(r'spine.jpg'),extent=[-210,247,-94,95],alpha=.8)
    
    splinex = []

    for i in range(1,len(trazadores[0])+1):
        splinex.append(simplify(sympify(trazadores[0][i-1])+sympify(trazadores[1][i-1])*(x-sympify(points[i-1][0]))+sympify(trazadores[2][i-1])*(x-sympify(points[i-1][0]))**2+sympify(trazadores[3][i-1])*(x-sympify(points[i-1][0]))**3))

    for i,(spline,color) in enumerate(zip(splinex,plt.cm.rainbow(np.linspace(0,1,len(splinex)))),start=1):
        s = lambdify(x,spline,'numpy')
        plt.plot(np.linspace(points[i-1][0],points[i][0],400),s(np.linspace(points[i-1][0],points[i][0],400)),label=fr'$S_{{{i}}}$',color=color)

    for (x_,y_),color in zip(points,plt.cm.rainbow(np.linspace(0,1,len(points)))):
        plt.scatter(x_,y_,color=color,s=50)

    plt.axhline(y=0,color='black',linewidth=1) 
    plt.axvline(x=0,color='black',linewidth=1)
    plt.xlim(-210,247)
    plt.ylim(-94,95)
    plt.xlabel('x')
    plt.ylabel(r'$S_i(x)$',rotation=0,labelpad=0)
    plt.grid(True,linestyle='--',alpha=.5)
    plt.title('trazadores cúbicos naturales'if(trazadores==natural())else('trazadores cúbicos sujetos'if(trazadores==sujeto())else'trazadores cúbicos'))
    plt.legend()
    plt.show()

while 1:

    system('cls' if name == 'nt' else 'clear')

    if(bool(int(input('1:natural,0:sujeto: ')))):
        print('trazadores cúbicos naturales\n')
        for i in range(1,len(natural()[0])+1):
            print(f'S_{i}(x) = {natural()[0][i-1]}+({natural()[1][i-1]})*(x-{points[i-2][0]})+({natural()[2][i-1]})*(x-{points[i-2][0]})^2+({natural()[3][i-1]})*(x-{points[i-2][0]})^3')
        splines(natural())

    else:
        print('trazadores cúbicos sujetos\n')
        for i in range(1,len(sujeto()[0])+1):
            print(f'S_{i}(x) = {sujeto()[0][i-1]}+({sujeto()[1][i-1]})*(x-{points[i-2][0]})+({sujeto()[2][i-1]})*(x-{points[i-2][0]})^2+({sujeto()[3][i-1]})*(x-{points[i-2][0]})^3')
        splines(sujeto())

    system('cls' if name == 'nt' else 'clear')

    if(bool(int(input('1:salir,0:continuar: ')))):
        system('cls' if name == 'nt' else 'clear')
        break
