import tqdm

def run_n(model, algorithm, iterations, save=True):
    """
    Run an algorithm n times and compile the results.
    """
    costs = []
    completions = []

    best_model = None
    lowest_cost = 1000000

    # Write costs and completions to a file.
    if save:
        file = open(f"outputs/test_{algorithm}.txt", 'a')

    for _ in tqdm.tqdm(range(iterations)):
        # Run solver
        solution = algorithm(model)
        solution.run(verbose=False)

        # Record results
        cost = solution.cost()
        completion = solution.completion()

        costs.append(cost)
        completions.append(completion)

        # Compare to best model found
        if cost < lowest_cost and completion == 1:
            best_model = solution
            lowest_cost = cost
    
        if save:
            file.write(str(cost) + ', ' + str(completion) + '\n')

    if save:
        file.close()
    
    return best_model, costs, completions
