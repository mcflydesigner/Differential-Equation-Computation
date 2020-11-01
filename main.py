from de import DifferentialEquation
from PyQt5.QtWidgets import QApplication
from controller import Controller
from ivp import IVP
import sys





if __name__ == '__main__':
    #After running the program set up everything
    ivp = IVP(1, 2)
    de = DifferentialEquation(ivp)

    #Start GUI
    app = QApplication(sys.argv)
    controller = Controller(ivp, 5, 10, 3, 10, de)
    sys.exit(app.exec())

