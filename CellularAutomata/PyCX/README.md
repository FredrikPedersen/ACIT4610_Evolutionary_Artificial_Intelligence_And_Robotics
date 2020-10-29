# PyCX - Covid-19 Cellular Automata Modelling

PyCX is a Python-based sample code repository for complex systems
research and education. This version of the PyCX simulator has been 
somewhat modified to fit the needs of the Covid-19 Cellular Automata Simulation.

All credit belongs to the original author Hiroki Sayama.
The original PyCX library is available from the **[Project
website](http://github.com/hsayama/PyCX/)**.

## What is PyCX?

The PyCX project aims to develop an online repository of simple,
crude, yet easy-to-understand Python sample codes for dynamic complex
systems modeling and simulation, including iterative maps, ordinary
and partial differential equations, cellular automata, network
analysis, dynamical networks, and agent-based models. You can run,
read and modify any of its codes to learn the basics of complex
systems modeling and simulation in Python.

The target audiences of PyCX are researchers and students who are
interested in developing their own software to study complex systems
using a general-purpose programming language but do not have much
experience in computer programming.

The core philosophy of PyCX is therefore placed on the simplicity,
readability, generalizability, and pedagogical values of sample
codes. This is often achieved even at the cost of computational speed,
efficiency, or maintainability. For example, PyCX does not use
object-oriented programming paradigms so much, it does not use
sophisticated but complicated algorithm or data structure, it *does*
use global variables frequently, and so on. These choices were
intentionally made based on the author's experience in teaching
complex systems modeling and simulation to non-computer scientists
coming from a wide variety of domains.

For more details of its philosophy and background, see the following
open-access article: Sayama, H. (2013) PyCX: A Python-based simulation
code repository for complex systems education. Complex Adaptive
Systems Modeling 1:2.  http://www.casmodeling.com/content/1/1/2

## How to use it?

1. Install Python 3 (or 2, if you want), numpy, scipy, matplotlib, and
NetworkX.

   Installers are available from the following websites:
   * http://python.org/
   * http://scipy.org/
   * http://matplotlib.org/
   * http://networkx.github.io/
  
   Alternatively, you can use prepackaged Python suites, such as:
   * [Anaconda Individual Edition](https://www.anaconda.com/products/individual)

   The codes were tested using Anaconda Individual Edition of Python 3.7
and 2.7 on their Spyder and Jupyter Notebook environments.

2. Choose a PyCX sample code of your interest.

3. Run it. To run a dynamic, interactive simulation, make sure you have [pycxsimulator.py](https://github.com/hsayama/PyCX/blob/master/pycxsimulator.py).

4. Read the code to learn how the model was implemented.

5. Change the code as you like.

*Note for Spyder users:* Dynamic simulations may cause a conflict with Spyder's own graphics backend. In such a case, go to "Run" -> "Configuration per file" and select "Execute in an external system terminal".

*Note for Jupyter Notebook users:* You can run PyCX codes by entering "%run sample-code-name" in your Notebook.
