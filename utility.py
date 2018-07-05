from numpy.polynomial.polynomial import polyfit
def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m

def getVal(test_point,x,y,plt=None):
    b,m=polyfit(x,y, 1)
    if plt is not None: plt.plot(x,[m*i+b for i in x])
    return m*test_point+b

def getRisidual(x,y):
    b,m=polyfit(x,y, 1)
    test_point=m*x[1]+b
    return y[1]-test_point

