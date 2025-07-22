import plotly.graph_objects as go

def render_radar_chart(data_dict, title):
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    # For closed radar shape
    values += values[:1]
    labels += labels[:1]

    fig = go.Figure(
        data=[
            go.Scatterpolar(r=values, theta=labels, fill='toself', name='Radar')
        ]
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title=title
    )
    return fig
