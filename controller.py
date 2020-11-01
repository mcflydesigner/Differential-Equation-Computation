from model import Model
from view import View
from accurancy import Accurancy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from ivp import IVP

class Controller:
    """
        Controller is a part of the MVC model.
        Controller accepts input from the user and handle them.
    """
    def __init__(self, ivp, X, n, n0, N, de):
        self.model = Model(ivp, X, n, n0, N, de)
        self.root = View(self)

        self.solveDEs()

    def setParameters(self, ivp, X, n, n0, N):
        """ A method to change current parameters of the model """
        self.model.ivp = ivp
        self.model.X = X
        self.model.n = n
        self.model.n0 = n0
        self.model.N = N
        #recalculate the const for DE
        self.model.de.setIVP(ivp)

    def solveDEs(self):
        """ Solve the DE using each method separately and return the solutions as objects """
        self.solutions = []

        #Solve the DE using each method
        for i in range(len(self.model.methods)):
            Method = self.model.methods[i]

            me = Method(self.model.de, self.model.X, self.model.n)
            me.solve()

            #For numerical methods find GTE and TAE respectively
            if Method in self.model.numerical_methods:
                gte = Accurancy.gte(me)
                setattr(me, 'gte', gte)
                tae = Accurancy.tae(me, self.model.n0, self.model.N)
                setattr(me, 'tae', tae)
                setattr(me, 'tae_n0', self.model.n0)
                setattr(me, 'tae_N', self.model.N)

            self.solutions.append(me)

        #After solving redraw all the charts in View
        self.root.plotCharts(self.solutions)

    def callBackChecBoxChanged(self, state):
        """ Handle changing of checkboxes in the View """

        #Find the checkbox which changed its state
        for i in range(len(self.root.checkBoxes)):
                 if self.root.sender() == self.root.checkBoxes[i]:
                     #We found the checkbox which changed its state, handle it
                     if (state == QtCore.Qt.Checked):
                         self.model.plotted[i] = 1
                     else:
                         self.model.plotted[i] = 0

        #Update all charts
        self.root.plotCharts(self.solutions)

    def callBackUpdateInput(self):
        """ Handle the button "Plot" when the user updates the input values """

        #Validate all input labels
        for lineEdit in self.root.ui_lineEdits:
            if lineEdit.text() == '':
                #Found an empty field
                QMessageBox.about(self.root, 'Error', 'Please fill all labels :)')
                return

        #Get values from the fields directly
        x0 = float(self.root.ui_lineEdits[0].text())
        y0 = float(self.root.ui_lineEdits[1].text())
        X = float(self.root.ui_lineEdits[2].text())
        n = int(self.root.ui_lineEdits[3].text())
        n0 = int(self.root.ui_lineEdits[4].text())
        N = int(self.root.ui_lineEdits[5].text())

        #Validation of the input data
        if x0 >= X:
            QMessageBox.about(self.root, 'Error', 'X must be greater than x0 :)')
            return
        if x0 <= 0:
            QMessageBox.about(self.root, 'Error', 'x0 must be a positive number :)')
        if X <= 0:
            QMessageBox.about(self.root, 'Error', 'X must be a positive number :)')
        if n < 2:
            QMessageBox.about(self.root, 'Error', 'n must be greater than 1 :)')
            return
        if n0 < 2:
            QMessageBox.about(self.root, 'Error', 'n0 must be greater than 1 :)')
            return
        if N <= n0:
            QMessageBox.about(self.root, 'Error', 'N must be greater than n0 :)')
            return

        #Try to solve the equation based on the input data
        #In case of Division by 0, the user will get the message
        try:
            self.setParameters(IVP(x0, y0), X, n, n0, N)
            self.solveDEs()
        except Exception as e:
            QMessageBox.about(self.root, 'Error', str(e) + ' Please, change the values :)')
            return


