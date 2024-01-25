import plotly.graph_objects as go

def test_data(X, Y):
    pass

def distribution(values):
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