import tqdm

def run_n(model, algorithm, iterations, save=True):
    """
    Run an algorithm n times and compile the results.
    """
    costs = []
    completions = []
    models = []

    if save:
        file = open(f"outputs/test{iterations}.txt", 'w')

    for i in tqdm.tqdm(range(iterations)):
        solution = algorithm(model, verbose=False)
        solution.run()

        cost = solution.cost()
        completion = solution.completion()

        models.append(solution)
        costs.append(cost)
        completions.append(completion)
    
        if save:
            file.write(str(cost) + ', ' + str(completion) + '\n')

    if save:
        file.close()
    
    return models, costs, completions
