from methods import ExactMethod

class Accurancy:
    """
        This class is used to calculate the 'Local Errors' and
        'Total Approximation Errors' for numerical methods.
    """

    @staticmethod
    def gte(method) -> []:
        """ Calculate the 'Local Errors' and return them """
        gtes = []

        for i in range(0, len(method._ys)):
            e = abs(method._de.getExactSolution(method._xs[i]) - method._ys[i])
            gtes.append(e)

        return gtes

    @staticmethod
    def tae(method, n0, N) -> []:
        """
            Calculate the 'Total Approximation Errors' in the given
            interval [n0, n] and return the values.
        """

        taes = [0] * (N-n0+1)
        typeOfMethod = type(method)

        for n in range(n0, N+1):
            tempMethod = typeOfMethod(method._de, method._X, n)
            tempMethod.solve()

            exactMethod = ExactMethod(method._de, method._X, n)
            exactMethod.solve()

            taes[n-n0] = max(abs(tempMethod._ys - exactMethod._ys))

        return taes