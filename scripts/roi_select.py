import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor
import argparse
from brukerapi.dataset import Dataset as ds

parser = argparse.ArgumentParser()
parser.add_argument("serie", type=np.int)
parser.add_argument("filename", type=np.str)

args = parser.parse_args()

dataset = ds("../data/{}/pdata/1/2dseq".format(getattr(args,"serie")))
data = np.array(dataset.data)
im = data[:,:,0,0]/np.amax(data[:,:,0,0])

x0 = 0
r = 0

circles = []
circle = []
y = []

def press(event):
    circle.append(event.xdata)
    y.append(event.ydata)

def draw(event):
    if event.button is not None:
        r = abs(event.xdata - circle[-1])
        circle_draw = plt.Circle((circle[-1], y[-1]), r, fc=None, ec='b', alpha=.6)
        ax.add_patch(circle_draw)
        plt.draw()
        plt.pause(0.1)
        [p.remove() for p in reversed(ax.patches)]

def release(event):
    circle.append(event.xdata)

def enter(event):
    if event.key == "enter":
        plt.close()

# Defino la figura
fig, ax = plt.subplots(figsize=(7, 4))

# Mostramos la imagen como un mapa de grises
ax.imshow(im, cmap='gray')
ax.axis('off')

# Agrego el cursor y conecto la accion de presionar a la funcion click
cursor = Cursor(ax, horizOn=False, vertOn=True, useblit=True,
                color='blue', linewidth=1)

fig.canvas.mpl_connect('button_press_event', press)
fig.canvas.mpl_connect('motion_notify_event', draw)
fig.canvas.mpl_connect('button_release_event', release)
fig.canvas.mpl_connect('key_press_event', enter)

ax.imshow(im)
plt.show()

for i in range(3):
    circle[2*i+1] = circle[2*i+1]-circle[2*i]

circle = [[int(x),int(y),int(r)] for x,y,r in zip(circle[0::2], y, circle[1::2])]
np.savetxt(getattr(args,"filename"), circle)