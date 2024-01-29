import random
import math

from .hillclimber import Hillclimber

class Simulated_Annealing(Hillclimber):
    def __init__(self, solver, temperature):
        super().__init__(solver)

        self.T0 = temperature
        self.T = temperature

    def update_temperature(self):
        self.T = self.T - (self.T0 / self.i)
        # alpha = 0.94
        # self.T = self.T * alpha
    
    def check_solution(self, new_solution):
        if new_solution.completion() == 1:
            new_cost = new_solution.cost()
            old_cost = self.current_solution.cost()
            delta = new_cost - old_cost

            probability = math.exp(-delta / self.T)

            if random.random() < probability:
                self.current_solution = new_solution
        
        self.check_best_solution()
        self.update_temperature()
    
    def __repr__(self):
        return "Simulated Annealing"