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
        model_instance = model.copy_model()

        algorithm(model_instance)

        cost = model_instance.total_cost()
        completion = model_instance.net_completion()

        models.append(model_instance)
        costs.append(cost)
        completions.append(completion)
    
        if save:
            file.write(str(cost) + ', ' + str(completion) + '\n')


    if save:
        file.close()
    
    return models, costs, completions
