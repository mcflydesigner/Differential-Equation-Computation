from methods import (ExactMethod,
                     EulerMethod,
                     ImprovedEulerMethod,
                     RungeKuttaMethod)

class Model:
    """
        Model is a part of MVC model.
        Model holds the data structure which the program is working with.
    """

    def __init__(self, ivp, X, n, n0, N, de):
        self.ivp = ivp
        self.X = X
        self.n = n
        self.n0 = n0
        self.N = N
        self.de = de

        self.numerical_methods = [EulerMethod, ImprovedEulerMethod, RungeKuttaMethod]
        self.methods = [ExactMethod] + self.numerical_methods

        #Initially, all checkboxes are set up as true for each method in the order:
        #EulerMethod / EulerMethod / ImprovedEulerMethod / RungeKuttaMethod
        self.plotted = [True, True, True, True]