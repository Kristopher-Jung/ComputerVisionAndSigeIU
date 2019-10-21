import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(211)

x = np.arange(0.0, 5.0, 0.01)
y = 1*np.ones(np.shape(x))

ax.plot(x, y, '-')
ax.set_ylim(-2, 2)
ax.set_title('Press left mouse button and drag to test')

ax2 = fig.add_subplot(212)
line2, = ax2.plot(x, y, '-')


def onselect1(xmin, xmax):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    thisx = x[indmin:indmax]
    thisy = y[indmin:indmax]
    print(thisx.shape, thisy.shape)
    line2.set_data(thisx, thisy)
    ax2.set_xlim(thisx[0], thisx[-1])
    ax2.set_ylim(thisy.min(), thisy.max())
    fig.canvas.draw_idle()

    # save
    np.savetxt("text.out", np.c_[thisx, thisy])

# set useblit True on gtkagg for enhanced performance
span = SpanSelector(ax, onselect1, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.show()