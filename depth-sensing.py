#!/usr/bin/env python2

# Crude mockup, just for presentation purposes

# Capturing deph matrix from Intel RealSense, without patching kernel:
# gst-launch-0.10 v4l2src device=/dev/video1 num-buffers=1 ! multifilesink location="v1.raw"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from scipy.ndimage.filters import *

import cv2

mymat = maximum_filter(np.fromfile("v1.raw", dtype='int16').reshape((480, 640)), size=(5, 5))

fig = plt.figure()
data = fig.add_subplot(221)
xsection = fig.add_subplot(223)
ysection = fig.add_subplot(222)
product = fig.add_subplot(224)

class LineBuilder:
    def __init__(self, xline, yline, binder, graph):
        self.xline = xline
        self.yline = yline
        self.graph = graph
        self.cid = binder.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes != self.graph.axes: return
        self.yline.set_data(np.arange(480), mymat[:, event.xdata])
        self.yline.figure.canvas.draw()

    self.xline.set_data(np.arange(640), mymat[event.ydata, :])
        self.xline.figure.canvas.draw()

xline, = xsection.plot(np.arange(640), mymat[300,:])
yline, = ysection.plot(np.arange(480), mymat[:,300])

class Selector2D:
   def __init__(self, myplot):
        self.plot = myplot 
    self.xr = None
    self.yr = None

   def xselect(self, xmin, xmax):
    self.xr = (min(xmin, xmax), max(xmin, xmax))
    self.update()

   def yselect(self, ymin, ymax):
    self.yr = (min(ymin, ymax), max(ymin, ymax))
    self.update()

   def update(self):
    print self.xr, self.yr
       if self.xr != None and self.yr != None:
        a = xline.get_ydata()[self.xr[0]:self.xr[1]]
            b = yline.get_ydata()[self.yr[0]:self.yr[1]]
        ar = np.array([a]).repeat(b.size, axis=0)
            br = np.array([b]).T.repeat(a.size, axis=1)
        c = ar + br

        self.plot.imshow(c).figure.canvas.draw()
            

selector = Selector2D(product)

sp1 = SpanSelector(xsection, selector.xselect, 'horizontal', useblit=True,
             rectprops=dict(alpha=0.5, facecolor='red'))
sp2 = SpanSelector(ysection, selector.yselect, 'horizontal', useblit=True,
             rectprops=dict(alpha=0.5, facecolor='red'))

lb = LineBuilder(xline, yline, fig, data.imshow(mymat))


plt.show()
