import random
import math

from .hillclimber import Hillclimber

class Simulated_Annealing(Hillclimber):
    """
    Simulated annealing algorithm that tries to improve the model like Hilllclimber.
    Each improvement is kept, but worse solutions have a chance to be kept as well
    based on the current temperature which decreases after each iteration.

    Shares a lot of code with the Hillclimber class.
    """
    def __init__(self, solver, temperature):
        super().__init__(solver)

        self.T0 = temperature
        self.T = temperature

    def update_temperature(self):
        """
        Update the temperature.
        Temperature decreases linearly.
        """
        self.T = self.T - (self.T0 / self.i)
    
    def check_solution(self, new_solution):
        """
        Saves a new solution based on how it performs against the current solution
        as well as the current temperature.
        """
        if new_solution.completion() == 1:
            new_cost = new_solution.cost()
            old_cost = self.current_solution.cost()
            delta = new_cost - old_cost

            # Probability based on difference of performance and current temperature.
            # Probability if new model is improvement is >1.
            probability = math.exp(-delta / self.T)

            if random.random() < probability:
                self.current_solution = new_solution
        
        # Update best solution and temperature.
        self.check_best_solution()
        self.update_temperature()
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return "Simulated Annealing"