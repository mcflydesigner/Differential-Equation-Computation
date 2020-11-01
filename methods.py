from abc import ABC, abstractmethod
import numpy as np

class Method(ABC):
    """ Abstract class for each method of solving DE """
    def __init__(self, de, X, n):
        self._de = de
        self._X = X
        self._n = n
        #Calculate the step
        self._h = (X - de.ivp.x0) / n
        self._xs = list(np.linspace(de.ivp.x0, X, n+1))
        self._ys = np.array([de.ivp.y0])
    @abstractmethod
    def solve(self):
        """ Function to solve the DE """
        pass
    @abstractmethod
    def getColor(self):
        """ The color will be used on the chart. """
        pass
    def getXs(self):
        """ Getter of x-coordinates of the method """
        return self._xs
    def getYs(self):
        """ Getter of y-coordinates of the method """
        return self._ys





class ExactMethod(Method):
    """
        Implementation of Exact Method for solving DE.
        This method is not numerical.
    """
    def __init__(self, de, X, n):
        super().__init__(de, X, n)


    def solve(self):
        for x in self._xs[1:]:
            y = self._de.getExactSolution(x)
            self._ys = np.append(self._ys, y)

    def getColor(self):
        return 'g'

    def __str__(self):
        return 'Exact'







class EulerMethod(Method):
    """
        Implementation of Euler Method for solving DE.
        This method is numerical.
    """

    def __init__(self, de, X, n):
        super().__init__(de, X, n)

    def solve(self):
        for x in self._xs[:-1]:
            y = self._ys[-1] + self._h * self._de.f(x, self._ys[-1])
            self._ys = np.append(self._ys, y)

    def getColor(self):
        return 'b'

    def __str__(self):
        return 'Euler'





class ImprovedEulerMethod(Method):
    """
        Implementation of Improved Euler Method for solving DE.
        This method is numerical.
    """

    def __init__(self, de, X, n):
        super().__init__(de, X, n)

    def solve(self):
        for x in self._xs[:-1]:
            y = self._ys[-1] + (self._h / 2) * ((self._de.f(x, self._ys[-1]) +
                                                 self._de.f(x + self._h, self._ys[-1] +
                                                            self._h * self._de.f(x, self._ys[-1]))))

            self._ys = np.append(self._ys, y)

    def getColor(self):
        return 'y'

    def __str__(self):
        return 'Improved Euler'






class RungeKuttaMethod(Method):
    """
            Implementation of Runge-Kutta Method for solving DE.
            This method is numerical.
        """

    def __init__(self, de, X, n):
        super().__init__(de, X, n)

    def solve(self):
        for x in self._xs[:-1]:
            k1 = self._de.f(x, self._ys[-1])
            k2 = self._de.f(x + self._h / 2, self._ys[-1] + (self._h / 2) * k1)
            k3 = self._de.f(x + self._h / 2, self._ys[-1] + (self._h / 2) * k2)
            k4 = self._de.f(x + self._h, self._ys[-1] + self._h * k3)

            y = self._ys[-1] + (self._h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            self._ys = np.append(self._ys, y)

    def getColor(self):
        return 'r'

    def __str__(self):
        return 'Runge-Kutta'
