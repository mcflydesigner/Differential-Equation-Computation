from abc import ABC, abstractmethod

class EquationInterface(ABC):
    """ Abstract class for interface for the equations """
    @abstractmethod
    def setIVP(self, IVP):
        pass

    @abstractmethod
    def f(self):
        pass

    @abstractmethod
    def getExactSolution(self):
        pass






class DifferentialEquation(EquationInterface):
    """ The class which is responsible for storing the info about DE """

    def __init__(self, ivp):
        self.ivp = ivp
        self.__setConst()




    def __setConst(self) -> None:
        """ Solve the IVP problem to find the const c for the solution of DE"""
        assert self.ivp.x0 > 0, 'x0 can not be negative'

        #Validate the IVP values
        if(((self.ivp.x0**2)*self.ivp.y0-self.ivp.x0) == 0):
            raise ValueError('Constant could not be found.')

        self.const = (self.ivp.x0 ** (4 / 3) * (self.ivp.x0 * self.ivp.y0 - 2)) / \
                     ((self.ivp.x0 ** 2) * self.ivp.y0 - self.ivp.x0)



    def __f(self, x, y) -> float:
        """
            Calculate the result of f(x,y) function for arguments: x, y.
            Then return the result.
        """

        #Validate the values
        if(x == 0):
            raise ValueError("Got division by 0. ")

        return -((y ** 2) / 3) - (2 / (3 * (x ** 2)))



    def __solutionDE(self, x, c) -> float:
        """
            Calculate the exact solution for x and c(const) arguments and return the result
        """

        #Validate the values
        if(((x**(4/3)) - c*x) == 0):
            raise ValueError("Got division by 0. ")

        return (2 / x) + c / ((x ** (4 / 3)) - c * x)




    def setIVP(self, ivp) -> None:
        """ Set new initial values for the DE """
        self.ivp = ivp
        self.__setConst()



    def f(self, x, y) -> float:
        """
            Calculate the exact solution for x and y arguments and return the result
        """
        return self.__f(x, y)




    def getExactSolution(self, x) -> float:
        """ Calculate the exact solution for x argument and return the result """
        return self.__solutionDE(x, self.const)
