import array
from math import nan

import plotly.graph_objects as go
from numpy import zeros


def plot_curves(x, y, z, color: str = "black", width=2):
    return go.Scatter3d(x=x, y=y, z=z, mode='lines', line={"color": color, "width": width}, showlegend=False)


def plot_dist(x, y, z, w, color: str = "jet", size: int = 2, opacity: float = 1.):
    return go.Scatter3d(x=x, y=y, z=z, mode='markers', showlegend=False,
                        marker=dict(size=size, color=w, colorscale=color, opacity=opacity, showscale=True))


def plot(*traces, camera=None, show_axes: bool = True, background_box=True):
    fig = go.Figure(layout=go.Layout(scene={'aspectmode': 'data'}))
    for trace in traces:
        fig.add_trace(trace)
    if camera is None:
        camera = {'eye': {'x': 1, 'y': -2, 'z': 1}}
    if not show_axes:
        fig.update_layout(
            scene=dict(
                xaxis=dict(title=' ', showticklabels=False),
                yaxis=dict(title=' ', showticklabels=False),
                zaxis=dict(title=' ', showticklabels=False),
            )
        )
    if not background_box:
        fig.update_layout(scene=dict(
            xaxis=dict(backgroundcolor="white"),
            yaxis=dict(backgroundcolor="white"),
            zaxis=dict(backgroundcolor="white"))
        )
    fig.update_layout(scene_camera=camera)
    return fig


def plot_pts(*xyzw: array):
    if len(xyzw) == 2:
        sys = plot_curves([0, 1], [0, 0], [0, 0])
        x, w = xyzw
        y = zeros(len(x))
        z = zeros(len(x))
        pts = plot_dist(x, y, z, w, size=8)
        plot(sys, pts).show()
    elif len(xyzw) == 3:
        sys = plot_curves([0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0])
        x, y, w = xyzw
        z = zeros(len(x))
        pts = plot_dist(x, y, z, w, size=8)
        plot(sys, pts).show()
    elif len(xyzw) == 4:
        sys = plot_curves([0, 1, 0, 0, 0, 1, nan, 0, 0], [0, 0, 1, 0, 0, 0, nan, 0, 1], [0, 0, 0, 0, 1, 0, nan, 1, 0])
        pts = plot_dist(*xyzw, size=8)
        plot(sys, pts).show()
