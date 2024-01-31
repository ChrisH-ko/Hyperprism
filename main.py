import random

from code.classes import chip
from code.classes import model as mod

from code.algorithms.functions import solve_model as solve
from code.algorithms.functions import experiment as exp

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import shortest_first_solver as sfs
from code.algorithms.netlist_solver import hardest_first_solver as hfs
from code.algorithms.netlist_solver import hillclimber as hc
from code.algorithms.netlist_solver import simulated_annealing as sa
from code.algorithms.netlist_solver import fix_crossings as fc


from code.analysis import testn as test

random.seed(0)

def get_chip():
    """
    Get chip and netlist from user input.
    """
    chip_id = None
    net_id = None

    # User input, chip and net
    print('\n \n')
    while chip_id is None:
        chip_id = input('enter chip_id: ')
    while net_id is None:
        net_id = input('enter net_id: ')
    
    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    # Create a chip and load in a netlist from our data
    return chip.Chip(chip_id, chip_file, net_id, netlist)


def get_action():
    """
    From user input, get the next course of action
    """
    print('\n')
    action = None

    # User input
    print('solve model, experiment or quit?')
    print(['solve', 'experiment', 'quit'])
    while action not in ['solve', 'experiment', 'quit']:
        action = input(': ')
    return action


if __name__ == "__main__":

    # Load chip from user input
    static_chip = get_chip()

    # Create a model from our chip to create the connections in
    model = mod.Model(static_chip)
    print(f'Cost lower bound: {model.lower_bound_cost()}')

    action = None
    solution = None
    history = []

    while action != 'quit':
        action = get_action()

        # Solve the model, save the solution and how it was solved
        if action == 'solve':
            solution, history = solve.solve_model(model, solution, history)
        
        # Carry out an experiment
        if action == 'experiment':
            solution, history = exp.run_experiment(model, solution, history)