import random
import tqdm

from .net_solver import Net_Solver

class Hillclimber():
    def __init__(self, solver):
        self.start_solution = solver

        self.current_solution = Net_Solver(
            self.start_solution.model,
            self.start_solution.nets
        )

        self.best_solution = Net_Solver(
            self.start_solution.model,
            self.start_solution.nets
        )

        self.progress = [self.start_solution.cost()]

    def current_model(self):
        return self.current_solution.model
    
    def current_nets(self):
        return self.current_solution.nets
    
    def reset_solution(self):
        self.current_solution = Net_Solver(
            self.start_solution.model,
            self.start_solution.nets
        )
    
    def mutate_nets(self):
        new_netlist = self.current_nets()

        old_loc = random.randint(0, len(new_netlist)-1)
        new_loc = random.randint(0, len(new_netlist)-1)

        net = new_netlist.pop(old_loc)
        new_netlist.insert(new_loc, net)
        return new_netlist
    
    def check_solution(self, new_solution):
        old_completion = self.current_solution.completion()
        new_completion = new_solution.completion()

        if new_completion >= old_completion:
            old_cost = self.current_solution.cost()
            new_cost = new_solution.cost()

            if new_cost <= old_cost:
                self.current_solution = new_solution

                self.check_best_solution()
    
    def check_best_solution(self):
        if self.current_solution.cost() <= self.best_solution.cost():
            self.best_solution = self.current_solution
     
    def run(self, i, pathfinder='standard', from_scratch=False, verbose=True):
        self.i = i
        iterations = self.check_verbose(verbose, self.i)

        for i in iterations:
            new_netlist = self.mutate_nets()
            new_solution = Net_Solver(self.current_model(), new_netlist)

            new_solution.run(
                pathfinder=pathfinder,
                from_scratch=from_scratch,
                verbose=False
                )

            self.progress.append(self.current_solution.cost())

            self.check_solution(new_solution)

    def check_verbose(self, verbose, i):
        if verbose:
            return tqdm.tqdm(range(i))
        return range(i)
    
    def __repr__(self):
        return 'Hillclimber'