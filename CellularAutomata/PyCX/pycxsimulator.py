import matplotlib
import matplotlib.pyplot as pyplot
import platform
import sys
import warnings
import covid_modelling.variables as variables
import covid_modelling.results.graph as graphs

if platform.system() == 'Windows':
    backend = 'TkAgg'
else:
    backend = 'Qt5Agg'
matplotlib.use(backend)

if sys.version_info[0] == 3:  # Python 3
    from tkinter import *
    from tkinter.ttk import Notebook
else:  # Python 2
    from Tkinter import *
    from ttk import Notebook

warnings.filterwarnings("ignore", category=matplotlib.cbook.MatplotlibDeprecationWarning)


class GUI:

    def __init__(self, title='Covid-19 Simulator', interval=0, stepSize=1, parameterSetters=[]):

        self.titleText = title
        self.timeInterval = interval
        self.stepSize = stepSize
        self.parameterSetters = parameterSetters
        self.varEntries = {}
        self.statusStr = ""

        self.running = False
        self.modelFigure = None
        self.currentStep = 0

        # create root window
        self.rootWindow = Tk()
        self.statusText = StringVar(self.rootWindow, value=self.statusStr)  # at this point, statusStr = ""
        self.setStatusStr("Simulation not yet started")

        self.rootWindow.wm_title(self.titleText)
        self.rootWindow.protocol('WM_DELETE_WINDOW', self.quitGUI)
        self.rootWindow.geometry('450x300')
        self.rootWindow.columnconfigure(0, weight=1)
        self.rootWindow.rowconfigure(0, weight=1)

        self.notebook = Notebook(self.rootWindow)
        self.notebook.pack(side=TOP, padx=2, pady=2)

        self.frameRun = Frame(self.rootWindow)
        self.notebook.add(self.frameRun, text="Run")
        self.notebook.pack(expand=NO, fill=BOTH, padx=5, pady=5, side=TOP)

        self.status = Label(self.rootWindow, width=40, height=3, relief=SUNKEN, bd=1, textvariable=self.statusText)
        self.status.pack(side=TOP, fill=X, padx=5, pady=5, expand=NO)

        # -----------------------------------
        # frameRun
        # -----------------------------------

        # buttonRun
        self.runPauseString = StringVar(self.rootWindow)
        self.runPauseString.set("Run")
        self.buttonRun = Button(self.frameRun, width=30, height=2, textvariable=self.runPauseString,command=self.runEvent)
        self.buttonRun.pack(side=TOP, padx=5, pady=5)
        self.showHelp(self.buttonRun, "Runs the simulation (or pauses the running simulation)")

        # buttonReset
        self.buttonReset = Button(self.frameRun, width=30, height=2, text='Reset', command=self.resetModel)
        self.buttonReset.pack(side=TOP, padx=5, pady=5)
        self.showHelp(self.buttonReset, "Resets the simulation")

        # buttonAdjustments
        self.adjustmentsEnabled = variables.ADJUSTMENTS_ENABLED

        self.toggleAdjustmentsString = StringVar(self.rootWindow)
        self.toggleAdjustmentsString.set("Disable Adjustments")
        if not self.adjustmentsEnabled:
            self.toggleAdjustmentsString.set("Enable Adjustments")

        self.buttonAdjustments = Button(self.frameRun, width=30, height=2, textvariable=self.toggleAdjustmentsString, command=self.toggleAdjustments)
        self.buttonAdjustments.pack(side=TOP, padx=5, pady=5)
        self.showHelp(self.buttonAdjustments, "Toggles simulation adjustments")

        # buttonQuit
        self.buttonQuit = Button(self.frameRun, width=30, height=2, text="Quit", command=self.quitGUI)
        self.buttonQuit.pack(side=TOP, padx=5, pady=5)
        self.showHelp(self.buttonQuit, "Exits the simulation")

    # <<<<< Init >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def setStatusStr(self, newStatus):
        self.statusStr = newStatus
        self.statusText.set(self.statusStr)

    # <<<< runEvent >>>>>
    # This event is envoked when "Run" button is clicked.
    def runEvent(self):
        self.running = not self.running
        if self.running:
            self.rootWindow.after(self.timeInterval, self.stepModel)
            self.runPauseString.set("Pause")
            self.buttonReset.configure(state=DISABLED)
            self.buttonAdjustments.configure(state=DISABLED)

            if len(self.parameterSetters) > 0:
                self.buttonSaveParameters.configure(state=NORMAL)
                self.buttonSaveParametersAndReset.configure(state=DISABLED)
        else:
            self.runPauseString.set("Continue Run")
            self.buttonReset.configure(state=NORMAL)
            self.buttonAdjustments.configure(state=NORMAL)

            if len(self.parameterSetters) > 0:
                self.buttonSaveParameters.configure(state=NORMAL)
                self.buttonSaveParametersAndReset.configure(state=NORMAL)

    def stepModel(self):
        if variables.EVOLUTION_COMPLETE:
            self.closeSimulation()
            self.drawGraphs()

        if self.currentStep >= variables.STEP_LIMIT:
            self.adjustModel()
            self.modelEvolve()
            return

        if self.running:
            self.modelStepFunc()
            self.currentStep += 1
            self.setStatusStr("Step " + str(self.currentStep))
            self.status.configure(foreground='black')
            if (self.currentStep) % self.stepSize == 0:
                self.drawModel()
            self.rootWindow.after(int(self.timeInterval * 1.0 / self.stepSize), self.stepModel)

    def resetModel(self, message="Model has been reset", manualReset = True):
        self.running = False
        self.runPauseString.set("Run")
        self.modelInitFunc()
        self.currentStep = 0
        self.adjustmentsEnabled = True

        if manualReset:
            variables.ADJUSTMENTS_ENABLED = False

        self.setStatusStr(message)
        self.drawModel()

    def adjustModel(self):
        self.modelAdjust()
        self.resetModel("Simulation Reached Current Date... adjusting", manualReset=False)
        self.runEvent()

    def toggleAdjustments(self):
        self.adjustmentsEnabled = not self.adjustmentsEnabled

        if not self.adjustmentsEnabled:
            self.toggleAdjustmentsString.set("Enable Adjustments")
        else:
            self.toggleAdjustmentsString.set("Disable Adjustments")

        variables.ADJUSTMENTS_ENABLED = self.adjustmentsEnabled

    def drawModel(self):
        pyplot.ion()

        if self.modelFigure is None or self.modelFigure.canvas.manager.window is None:
            self.modelFigure = pyplot.figure("Covid-19 Simulator")

        self.modelDrawFunc()
        self.modelFigure.canvas.manager.window.update()
        pyplot.show()

    def start(self, graph_data, func=[]):
        if len(func) == 5:
            self.modelInitFunc = func[0]
            self.modelDrawFunc = func[1]
            self.modelStepFunc = func[2]
            self.modelAdjust = func[3]
            self.modelEvolve = func[4]

            self.graphData = graph_data

            if (self.modelInitFunc.__doc__ != None and len(self.modelInitFunc.__doc__) > 0):
                self.textInformation.config(state=NORMAL)
                self.textInformation.delete(1.0, END)
                self.textInformation.insert(END, self.modelInitFunc.__doc__.strip())
                self.textInformation.config(state=DISABLED)

            self.modelInitFunc()
            self.drawModel()
        self.rootWindow.mainloop()

    def quitGUI(self):
        self.running = False
        self.rootWindow.quit()
        pyplot.close('all')
        self.rootWindow.destroy()

    def showHelp(self, widget, text):
        def setText(self):
            self.statusText.set(text)
            self.status.configure(foreground='blue')

        def showHelpLeave(self):
            self.statusText.set(self.statusStr)
            self.status.configure(foreground='black')

        widget.bind("<Enter>", lambda e: setText(self))
        widget.bind("<Leave>", lambda e: showHelpLeave(self))

    def closeSimulation(self):
        self.running = False
        pyplot.close("Covid-19 Simulator")
        self.buttonRun.configure(state=DISABLED)

    def drawGraphs(self):
        graphs.draw_graphs(self.graphData)

