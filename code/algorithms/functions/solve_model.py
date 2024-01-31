from code.visualization import visualize as vis

from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import shortest_first_solver as sfs
from code.algorithms.netlist_solver import hardest_first_solver as hfs

from code.algorithms.path_solver.standard_astar_alg import Standard_pathwise_astar
from code.algorithms.path_solver.make_space_astar import Make_Space

netsolvers = {
    'standard':ns.Net_Solver,
    'random':ns.Random_Net_Order,
    'shortest_first':sfs.Shortest_Net_Order,
    'hardest_first':hfs.Hardest_Net_Order
}
pathfinders = {
    'standard':Standard_pathwise_astar,
    'make_space': Make_Space
    }

text_bar = '-'*40


def start_solver(model, ns, pf, from_scratch):
    """
    Run a netsolver with an accompanying pathfinder on the give model.
    """
    print('\n')
    print(text_bar + ns)
    print(text_bar + pf)

    netsolver = netsolvers[ns]
    pathfinder = pathfinders[pf]

    solver = netsolver(model)
    solver.run(pathfinder=pathfinder, from_scratch=from_scratch)
    solver.results()

    return solver


def display_solution(solution, history):
    """
    Display the provided solution upon user request.
    """
    visualize = None
    print(f"Show solution? \n{['y', 'n']}")
    while visualize not in ['y', 'n']:
        visualize = input(': ')

        if visualize == 'y':
            vis.visualize(solution.model, history)


def check_existing_solution(model, solution, history):
    """
    Check whether a solution has already been made and whether to override it.
    """
    if solution is not None:
        print('\n \n')
        print('Solution has already been found: ')
        solution.results()

        display_solution(solution, history)

        answer = None
        print(f"Rewire existing solution? \n {['y', 'n']}")
        while answer not in ['y', 'n']:
            answer = input(': ')
        
        # Returns the solved model if yes, clears history if no
        if answer == 'y':
            return solution.model, history
        if answer == 'n':
            history = []
            return model, history
    
    return model, history


def get_algorithm(type):
    """
    Asks the user which algorithm should be used from the type that has been provided.
    """
    if type == 'net':
        name, choices = 'netsolver', list(netsolvers.keys())
    elif type == 'path':
        name, choices = 'pathfinder', list(pathfinders.keys())

    algorithm = None
    print(f'Which {name}? \n{choices}')
    while algorithm not in choices:
        algorithm = input(': ')
    
    return algorithm


def solve_model(model, solution, history):
    """
    Starts the model solver after selecting a netsolver and pathfinder.
    """
    # Check if solution already exists.
    model, history = check_existing_solution(model, solution, history)

    print('\n \n')
    
    # Get netsolver and pathfinder
    netsolver = get_algorithm('net')
    pathfinder = get_algorithm('path')
    
    # Check if we are rewiring an existing solution
    from_scratch = True
    if len(history) > 0:
        from_scratch = False
    
    # Start solving the model
    solver = start_solver(model, netsolver, pathfinder, from_scratch)

    # Add the algorithms used to the history
    history.append(f'{netsolver}+{pathfinder}')

    # Display the solution
    display_solution(solver, history)

    return solver, history