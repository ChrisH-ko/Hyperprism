import tqdm

def run_1000(model, algorithm, save=True):
    """
    Run an algorithm 1000 times and compile the results.
    """
    costs = []
    completions = []
    models = []

    if save:
        file = open("outputs/test1000.txt", 'w')

    for i in tqdm.tqdm(range(150)):
        solution = algorithm(model)

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
