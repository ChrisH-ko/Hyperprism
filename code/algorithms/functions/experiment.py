from code.algorithms.functions import solve_model as solve

from code.analysis import testn as test
from code.visualization import display_data as disp

from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import hillclimber as hc
from code.algorithms.netlist_solver import simulated_annealing as sa

def get_iterations():
    """
    Ask how many iterations an experiment should run.
    """
    i = -1
    print('How many iterations should the baseline algorithm run?')
    while i < 1:
        i = int(input(': '))
    
    return i


def plot_results(values, function):
    """
    Graph the results of an experiment, using the provided values and function.
    """
    display_results = None
    print(f"Display results? \n {['y', 'n']}")
    while display_results not in ['y', 'n']:
        display_results = input(': ')

    if display_results == 'y':
        function(values)


def best_solution(solution, algorithm):
    """
    Display the experiment's best solution.
    """
    print('\n Best solution:')
    solution.results()

    solve.display_solution(solution, algorithm)


def baseline_test(model, i):
    """
    Baseline experiment.

    Runs the random netsolver and standard pathfinder i times and records the
    costs of the different solutions.
    """
    best, costs, comp = test.run_n(model, ns.Random_Net_Order, i, save=True)

    results = [cost for cost, cmp in zip(costs, comp) if cmp == 1]
    return best, results


def hillclimb_test(solution, pathfinder, from_scratch, i):
    """
    Hillclimber experiment.

    Takes an existing solution and tries to improve upon it using the
    hillclimber algorithm. Results are saved in the hillclimber object.
    """
    climber = hc.Hillclimber(solution)
    climber.run(i, pathfinder=pathfinder, from_scratch=from_scratch, verbose=True)

    best = climber.best_solution
    return best, climber


def simanneal_test(solution, pathfinder, from_scratch, i):
    """
    Simanneal experiment.

    Takes and existing algorithm and tries to improve upon it using the 
    simulated annealing algorithm. Results are saved in the simulated annealing
    object.
    """
    simmaneal = sa.Simulated_Annealing(solution, temperature=500)
    simmaneal.run(i, pathfinder=pathfinder, from_scratch=from_scratch, verbose=True)
    
    best = simmaneal.best_solution
    return best, simmaneal

# Dicts to save the experiments and their respective functions
tests = {'baseline':baseline_test,
         'hillclimber':hillclimb_test,
         'simanneal':simanneal_test}

functions = {'baseline':disp.distribution,
         'hillclimber':disp.cost_decrease,
         'simanneal':disp.cost_decrease}


def run_experiment(model, solution, history):
    """
    Run an experiment based on user input
    """
    print('\n \n')

    # Get the desired experiment from user input
    experiment = None
    print(f"Choose an experiment: \n{list(tests.keys()) + ['return']}")
    while experiment not in list(tests.keys()) + ['return']:
        experiment = input(': ')
    
    if experiment != 'return':
        i = get_iterations()

        # Run experiment
        if experiment == 'baseline':
            solution, results = baseline_test(model, i)
        
        # Hillclimber/simulated annealing
        else:
            # Check whether to rewire the existing model or not.
            model, history = solve.check_existing_solution(model, solution, history)
            from_scratch = True
            if len(history) > 0:
                from_scratch = False

            # Get pathfinder
            pathfinder = solve.get_algorithm('path')
            
            # Run algorithm
            solution, results = tests[experiment](solution, solve.pathfinders[pathfinder], from_scratch, i)
        
        history.append(experiment)

        # Show results
        plot_results(results, functions[experiment])

        # Show best model
        best_solution(solution, [experiment])
    
    return solution, history