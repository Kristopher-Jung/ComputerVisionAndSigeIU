import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(211)

x = np.arange(0.0, 5.0, 0.01)
y = np.sin(2*np.pi*x) + 0.5*np.random.randn(len(x))

ax.plot(x, y, '-')
ax.set_ylim(-2, 2)
ax.set_title('Press left mouse button and drag to test')

ax2 = fig.add_subplot(212)
line2, = ax2.plot(x,y,'-')


def onselect(eclick, erelease):
    #indmin, indmax = np.searchsorted(x, (xmin, xmax))
    #indmax = min(len(x) - 1, indmax)
    minx = eclick.xdata
    maxx = erelease.xdata
    miny = eclick.ydata
    maxy = erelease.ydata
    indminx, indmaxx = np.searchsorted(x, (minx, maxx))
    indmaxx = min(len(x) - 1, indmaxx)
    indminy, indmaxy = np.searchsorted(y, (miny, maxy))
    indmaxy = min(len(y) - 1, indmaxy)
    thisx = x[indminx:indmaxx]
    thisy = y[indminy:indmaxy]
    print(thisx.shape, thisy.shape)

    line2.set_data(thisx, thisy)
    ax2.set_xlim(thisx[0], thisx[-1])
    ax2.set_ylim(thisy.min(), thisy.max())
    fig.canvas.draw_idle()


    # save
    #np.savetxt("text.out", np.c_[thisx, thisy])

    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)


# set useblit True on gtkagg for enhanced performance
span = RectangleSelector(ax, onselect, drawtype='box', interactive=True)



plt.show()