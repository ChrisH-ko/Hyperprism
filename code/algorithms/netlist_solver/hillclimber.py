import random
import tqdm

from code.algorithms.path_solver.standard_astar_alg import Standard_pathwise_astar
from .net_solver import Net_Solver

class Hillclimber():
    """
    Hillclimber algorithm.

    Takes a solved model and its net order, changes the position of one net and resolves the
    model. If a change improves the cost, it is kept.
    """
    def __init__(self, solver):
        if not solver.model.complete():
            raise Exception('This algorithm requires a solution.')
        
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
        """
        Returns the current model.
        """
        return self.current_solution.model
    

    def current_nets(self):
        """
        Returns the current model's net order.
        """
        return self.current_solution.nets
    

    def reset_solution(self):
        """
        Resets the current model back to the starting model.
        """
        self.current_solution = Net_Solver(
            self.start_solution.model,
            self.start_solution.nets
        )
    

    def mutate_nets(self):
        """
        Changes the position of a random net in the net order and returns it.
        """
        new_netlist = self.current_nets()

        old_loc = random.randint(0, len(new_netlist)-1)
        new_loc = random.randint(0, len(new_netlist)-1)

        net = new_netlist.pop(old_loc)
        new_netlist.insert(new_loc, net)
        return new_netlist
    

    def get_new_model(self, nets):
        """
        Returns a new solver from the current ont.
        """
        return Net_Solver(self.current_model(), nets)
    

    def check_solution(self, new_solution):
        """
        Checks whether the given solution is better than the current one.
        """
        old_completion = self.current_solution.completion()
        new_completion = new_solution.completion()

        # Discards the new solution if it has less completed nets.
        if new_completion >= old_completion:
            old_cost = self.current_solution.cost()
            new_cost = new_solution.cost()

            # Compare total costs.
            if new_cost <= old_cost:
                self.current_solution = new_solution

                # Check whether it is also the best.
                self.check_best_solution()
    

    def check_best_solution(self):
        """
        Check whether the current solution is also the best solution.
        """
        if self.current_solution.cost() <= self.best_solution.cost():
            self.best_solution = self.current_solution
    
    
    def run(self, i, pathfinder=Standard_pathwise_astar, from_scratch=False, verbose=True):
        """
        Run the algorithm for i iterations.
        """
        self.i = i
        iterations = self.check_verbose(verbose, self.i)

        for i in iterations:
            # Create new solver.
            new_netlist = self.mutate_nets()
            new_solution = self.get_new_model(new_netlist)

            # Run new solver.
            new_solution.run(
                pathfinder=pathfinder,
                from_scratch=from_scratch,
                verbose=False
                )

            # Save new cost.
            self.progress.append(self.current_solution.cost())

            # Comparenew solution with current one.
            self.check_solution(new_solution)


    def check_verbose(self, verbose, i):
        """
        Returns progress bar if verbose is True.
        """
        if verbose:
            return tqdm.tqdm(range(i))
        return range(i)
    
    
    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return 'Hillclimber'