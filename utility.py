def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m
