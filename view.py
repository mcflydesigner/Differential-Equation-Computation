from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    """ The chart for each tab """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)







class TabsWidget(QWidget):
    """ All tabs for the main screen. """

    def __init__(self, parent):
        super(TabsWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Initialize tab screen
        tabs = QTabWidget()
        self.tab_solutions = QWidget()
        self.tab_gte = QWidget()
        self.tab_tae = QWidget()
        tabs.resize(300, 300)

        #Add a figure for each tab
        self.figures = []
        for i in range(3):
            self.figures.append(MplCanvas(self, width=5, height=4, dpi=100))

        # Add 3 tabs
        tabs.addTab(self.tab_solutions, 'Solutions')
        tabs.addTab(self.tab_gte, 'Local Errors')
        tabs.addTab(self.tab_tae, 'Total Approximation Errors')
        layout.addWidget(tabs)
        self.setLayout(layout)

        #Set up the 1st tab
        self.__setUpSolutionsTab()

        #Set up the 2nd tab
        self.__setUpGTETab()

        #Set up the 3rd tab
        self.__setUpTAETab()




    def __setUpSolutionsTab(self) -> None:
        """ Set up the 1st tab """
        self.tab_solutions.layout = QVBoxLayout(self)

        toolbar = NavigationToolbar(self.figures[0], self)

        self.tab_solutions.layout.addWidget(self.figures[0])
        self.tab_solutions.layout.addWidget(toolbar)
        self.tab_solutions.setLayout(self.tab_solutions.layout)




    def __setUpGTETab(self) -> None:
        """ Set up the 2nd tab """
        self.tab_gte.layout = QVBoxLayout(self)

        toolbar = NavigationToolbar(self.figures[1], self)

        self.tab_gte.layout.addWidget(self.figures[1])
        self.tab_gte.layout.addWidget(toolbar)
        self.tab_gte.setLayout(self.tab_gte.layout)


    def __setUpTAETab(self) -> None:
        """ Set up the 3rd tab """
        self.tab_tae.layout = QVBoxLayout(self)

        toolbar = NavigationToolbar(self.figures[2], self)

        self.tab_tae.layout.addWidget(self.figures[2])
        self.tab_tae.layout.addWidget(toolbar)
        self.tab_tae.setLayout(self.tab_tae.layout)







class View(QtWidgets.QMainWindow):
    """
        View is a part of MVC model.
        View is the representation of graphical information as shown to the user.
    """

    def __init__(self, controller):
        super(View, self).__init__()
        self.setWindowTitle('DE Solver')
        self.controller = controller

        #Set up tabs
        self.table_widget = TabsWidget(self)
        #Set up user's input
        self.__setUpUserInput()

        layout = QHBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.__input_w)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()




    def __setUpUserInput(self) -> None:
        """ Set up the widget with user's input data """

        # User's input
        self.__layout_input = QVBoxLayout()

        #Set up input's labels with the text
        self.__layout_input.addWidget(QLabel('Input data:'))
        self.__ui_lineEdit_x0 = QLineEdit(str(self.controller.model.ivp.x0))
        self.__ui_lineEdit_y0 = QLineEdit(str(self.controller.model.ivp.y0))
        self.__ui_lineEdit_X = QLineEdit(str(self.controller.model.X))
        self.__ui_lineEdit_n = QLineEdit(str(self.controller.model.n))
        self.__ui_lineEdit_n0 = QLineEdit(str(self.controller.model.n0))
        self.__ui_lineEdit_N = QLineEdit(str(self.controller.model.N))

        self.ui_lineEdits = [self.__ui_lineEdit_x0, self.__ui_lineEdit_y0, self.__ui_lineEdit_X,
                             self.__ui_lineEdit_n, self.__ui_lineEdit_n0, self.__ui_lineEdit_N]

        self.__ui_labels = [QLabel('x0'), QLabel('y0'), QLabel('X'),
                            QLabel('n'), QLabel('n0'), QLabel('N')]

        #For the first three parameters set up the double validator
        for i in range(3):
            self.ui_lineEdits[i].setValidator(QtGui.QDoubleValidator())

        #For others int validator
        for i in range(3, len(self.ui_lineEdits)):
            self.ui_lineEdits[i].setValidator(QtGui.QIntValidator())

        #Connect each label with its relative input label
        for label, lineEdit in zip(self.__ui_labels, self.ui_lineEdits):
            self.__layout_input.addWidget(label)
            self.__layout_input.addWidget(lineEdit)

        #Add button to "Plot" the graph
        self.__buttonPlot = QPushButton('Plot everything :)')
        self.__buttonPlot.clicked.connect(self.controller.callBackUpdateInput)
        self.__layout_input.addWidget(self.__buttonPlot)
        self.__layout_input.addWidget(QLabel('Displaying of methods:'))

        #Add a checkbox for each method and set up them
        self.checkBoxes = []
        for method in self.controller.model.methods:
            self.checkBoxes.append(QCheckBox(method.__str__(method), self))

        for checkBox in self.checkBoxes:
            checkBox.setChecked(True)
            checkBox.stateChanged.connect(self.controller.callBackChecBoxChanged)
            self.__layout_input.addWidget(checkBox)


        self.__input_w = QWidget()
        self.__input_w.setLayout(self.__layout_input)
        self.__input_w.setFixedWidth(150)
        self.__input_w.setFixedHeight(450)




    def plotCharts(self, solutions) -> None:
        """ Plot the chart for each tab. """
        for figure in self.table_widget.figures:
            figure.axes.clear()

        for i in range(len(self.controller.model.methods)):
            #Skip the method if the checkbox is False
            if not self.controller.model.plotted[i]:
                continue

            #Plot the charts
            #1st tab with solutions
            xs = solutions[i].getXs()
            ys = solutions[i].getYs()
            color = solutions[i].getColor()
            label = solutions[i].__str__()

            self.table_widget.figures[0].axes.plot(xs, ys, color, label=label)
            self.table_widget.figures[0].axes.set_xlabel("x")
            self.table_widget.figures[0].axes.set_ylabel("y")
            self.table_widget.figures[0].axes.legend()

            #2nd tab with GTE
            if hasattr(solutions[i], 'gte'):
                gte = solutions[i].gte
                color = solutions[i].getColor()
                label = solutions[i].__str__()

                self.table_widget.figures[1].axes.plot(xs, gte, color, label=label)
                self.table_widget.figures[1].axes.set_xlabel("x")
                self.table_widget.figures[1].axes.set_ylabel("GTE")
                self.table_widget.figures[1].axes.legend()

            #3rd tab with TAE
            if hasattr(solutions[i], 'tae') and hasattr(solutions[i], 'tae_n0')\
                    and hasattr(solutions[i], 'tae_N'):

                tae = solutions[i].tae
                ns = [x for x in range(solutions[i].tae_n0, solutions[i].tae_N + 1)]
                color = solutions[i].getColor()
                label = solutions[i].__str__()

                self.table_widget.figures[2].axes.plot(ns, tae, color, label=label)
                self.table_widget.figures[2].axes.set_xlabel("n")
                self.table_widget.figures[2].axes.set_ylabel("Max GTE")
                self.table_widget.figures[2].axes.legend()

        #Update each canvas
        for figure in self.table_widget.figures:
            figure.draw_idle()
