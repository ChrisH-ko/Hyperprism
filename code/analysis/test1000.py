import tqdm

def run_1000(model, algorithm):
    """
    Run an algorithm 1000 times and compile the results.
    """
    costs = []
    completions = []
    models = []

    for i in tqdm.tqdm(range(50)):
        model_instance = model.copy_model()

        algorithm(model_instance)

        models.append(model_instance)
        costs.append(model_instance.total_cost())
        completions.append(model_instance.net_completion())
    
    return models, costs, completions
