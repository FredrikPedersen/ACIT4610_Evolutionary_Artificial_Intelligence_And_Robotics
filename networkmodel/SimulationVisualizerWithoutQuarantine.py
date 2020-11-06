from NetworkModel import *

visualizer = Visualizer()
pycxsimulator.GUI().start(func=[visualizer.initialize, visualizer.observe, visualizer.update_assuming_no_quarantine])