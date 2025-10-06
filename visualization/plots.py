import plotly.graph_objects as go


def plot_lap_times(lap_times, pit_stops=None, title="Lap Times vs Lap Number"):
    fig = go.Figure()

    # Line chart for lap times
    fig.add_trace(go.Scatter(
        y=lap_times,
        x=list(range(1, len(lap_times) + 1)),
        mode="lines+markers",
        name="Lap Time"
    ))

    # Add vertical lines for pit stops
    if pit_stops:
        for pit in pit_stops:
            fig.add_vline(
                x=pit,
                line=dict(color="red", dash="dash"),
                annotation_text="Pit Stop",
                annotation_position="top right"
            )

    fig.update_layout(
        title=title,
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        template="plotly_white"
    )

    return fig


def plot_tire_wear(tire_history, pit_stops=None, title="Tire Wear vs Lap Number"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=tire_history,
        x=list(range(1, len(tire_history) + 1)),
        mode="lines+markers",
        name="Tire Condition"
    ))
    if pit_stops:
        for pit in pit_stops:
            fig.add_vline(
                x=pit,
                line=dict(color="orange", dash="dot"),
                annotation_text="Pit Stop",
                annotation_position="top right"
            )
    fig.update_layout(
        title=title,
        xaxis_title="Lap Number",
        yaxis_title="Tire Condition",
        template="plotly_white"
    )
    return fig


def plot_fuel(fuel_history, pit_stops=None, title="Fuel Level vs Lap Number"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=fuel_history,
        x=list(range(1, len(fuel_history) + 1)),
        mode="lines+markers",
        name="Fuel Level"
    ))
    if pit_stops:
        for pit in pit_stops:
            fig.add_vline(
                x=pit,
                line=dict(color="blue", dash="dot"),
                annotation_text="Pit Stop",
                annotation_position="top right"
            )
    fig.update_layout(
        title=title,
        xaxis_title="Lap Number",
        yaxis_title="Fuel Level (%)",
        template="plotly_white"
    )
    return fig