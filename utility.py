from numpy.polynomial.polynomial import polyfit
def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m

def getVal(val,x,y):
    b,m=polyfit(x,y, 1)
    return m*val+b
