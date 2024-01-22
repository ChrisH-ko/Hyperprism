import plotly.graph_objects as go

def test_data(X, Y):
    pass

def distribution(values):
    fig = go.Figure(data=[go.Histogram(x=values)])
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                range=[0, max(values)]
            )
        )
    )
    fig.show()