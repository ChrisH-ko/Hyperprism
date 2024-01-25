import tqdm

def run_n(model, algorithm, iterations, save=True):
    """
    Run an algorithm n times and compile the results.
    """
    costs = []
    completions = []

    best_model = None
    lowest_cost = 100000

    if save:
        file = open(f"outputs/test{iterations}.txt", 'a')

    for i in tqdm.tqdm(range(iterations)):
        solution = algorithm(model, verbose=False)
        solution.run()

        cost = solution.cost()
        completion = solution.completion()

        costs.append(cost)
        completions.append(completion)

        if cost < lowest_cost:
            best_model = solution
            lowest_cost = cost
    
        if save:
            file.write(str(cost) + ', ' + str(completion) + '\n')

    if save:
        file.close()
    
    return best_model, costs, completions
