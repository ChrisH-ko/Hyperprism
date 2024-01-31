import plotly.graph_objects as go
import csv

def load_txt(filepath):
    """
    Load in a text file containing the data from an experiment.
    """
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            row = tuple(row)
            cost = int(row[0])
            completion = int(float(row[1]))

            if completion == 1:
                data.append(cost)
    f.close()
    return data

def distribution(values):
    """
    Display a distribution of costs.
    """
    fig = go.Figure(data=[go.Histogram(x=values,
                                       xbins=dict(
                                           size=500
                                       ))])
    fig.update_layout(
        title=f'Shuffled netlist, {len(values)} iterations',
        xaxis_title='Cost',
        yaxis_title='Count',
        bargap=0.1,
        scene=dict(
            xaxis=dict(
                range=[0, max(values)]
            )
        ),
        font=dict(
            size=16
        ),
    )
    fig.show()

def cost_decrease(climber):
    """
    Display the change in cost of a climber algorithm.
    """

    fig = go.Figure()

    # --------------------------------- Best costs ------------------
    x = [i for i in range(len(climber.current_costs))]
    best_y = climber.current_costs

    fig.add_trace(go.Scatter(x=x, y=best_y,
                                     mode='lines',
                                     name='best Cost',
                                     line=dict(
                                         color='red',
                                         width=4
                                     )))

    # ---------------------------- Cost at each iteration -----------
    y = climber.new_costs

    fig.add_trace(go.Scatter(x=x, y=y,
                                     mode='lines',
                                     name='Cost',
                                     line=dict(
                                         color='grey',
                                         width=2
                                     )))
    fig.update_layout(
        title=f'{climber}, {len(x)} iterations',
        xaxis_title='Iterations',
        yaxis_title='Cost',
        font=dict(
            size=16
        ),
    )

    fig.show()