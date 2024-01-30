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
    visualize = None
    print(f"Show solution? \n{['y', 'n']}")
    while visualize not in ['y', 'n']:
        visualize = input(': ')

        if visualize == 'y':
            vis.visualize(solution.model, history)

def check_existing_solution(model, solution, history):
    if solution is not None:
        print('\n \n')
        solution.results()

        display_solution(solution, history)

        answer = None
        print(f"Rewire existing solution? \n {['y', 'n']}")
        while answer not in ['y', 'n']:
            answer = input(': ')
        
        if answer == 'y':
            return solution.model, history
        if answer == 'n':
            history = []
            return model, history
    
    return model, history

def solve_model(model, solution, history):
    model, history = check_existing_solution(model, solution, history)

    print('\n \n')

    netsolver = None
    print(f'Which netsolver? \n{list(netsolvers.keys())}')
    while netsolver not in list(netsolvers.keys()):
        netsolver = input(': ')
    
    pathfinder = None
    print(f'Which pathfinder? \n{list(pathfinders.keys())}')
    while pathfinder not in list(pathfinders.keys()):
        pathfinder = input(': ')
    
    from_scratch = True
    if len(history) > 0:
        from_scratch = False
    
    solver = start_solver(model, netsolver, pathfinder, from_scratch)

    history.append(f'{netsolver}+{pathfinder}')

    display_solution(solver, history)

    return solver, history