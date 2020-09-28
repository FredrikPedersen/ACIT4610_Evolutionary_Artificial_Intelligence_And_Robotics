import PyCX.pycxsimulator as pycx
from pylab import *

areaDimensions: int = 10
initProb: float = 0.01
infectionRate: float = 0.5
recoveryRate: float = 0.15


def initialize():
    global time, config, nextConfig

    time = 0

    config = zeros([areaDimensions, areaDimensions])
    for posX in range(areaDimensions):
        for posY in range(areaDimensions):
            if random() < initProb:
                state = 2   # Infected
            else:
                state = 1   # Healthy

            config[posY, posX] = state

    nextConfig = zeros([areaDimensions, areaDimensions])


def observe():
    cla()
    imshow(config, vmin=0, vmax=2, cmap=cm.jet)
    axis('image')
    title('t = ' + str(time))


def update():
    global time, config, nextConfig

    time += 1

    for x in range(areaDimensions):
        for y in range(areaDimensions):

            state = config[y, x]

            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % areaDimensions, (x + dx) % areaDimensions] == 1:
                            if random() < recoveryRate:
                                state = 1

            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % areaDimensions, (x + dx) % areaDimensions] == 2:
                            if random() < infectionRate:
                                state = 2

            else:
                state = 0   # Dead/Recovering

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config


pycx.GUI().start(func=[initialize, observe, update])