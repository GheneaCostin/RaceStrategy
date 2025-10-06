import streamlit as st


def sidebar_controls():
    st.sidebar.title("Race Strategy AI Controls")

    # Track selection
    track = st.sidebar.selectbox(
        "Select Track",
        ["Monaco", "Silverstone", "Spa", "Monza", "Barcelona"]
    )

    # Weather conditions
    weather = st.sidebar.selectbox(
        "Weather Conditions",
        ["Sunny", "Rain", "Variable"]
    )

    # Tire compound selection (multi-stint)
    tires = st.sidebar.multiselect(
        "Tire Compound Selection (Stints)",
        ["Soft", "Medium", "Hard"],
        default=["Soft"]
    )

    # Fuel load
    fuel = st.sidebar.slider("Fuel Load (%)", 50, 100, 100)

    # Number of laps
    total_laps = st.sidebar.slider("Total Laps", min_value=5, max_value=70, value=20)

    # Pit Stop Strategy Mode
    strategy_mode = st.sidebar.radio("Pit Stop Strategy Mode", ["Manual", "AI Optimized"])

    # Number of simulation runs (Monte Carlo)
    num_runs = st.sidebar.slider("Number of Simulation Runs", 1, 100, 1)

    # Manual Stints Configuration
    pit_laps = []
    if strategy_mode == "Manual" and tires:
        st.sidebar.markdown("### Manual Stints Configuration")
        st.sidebar.write("Assign pit stop laps for each stint")
        for i in range(len(tires) - 1):
            lap = st.sidebar.number_input(
                f"Pit stop lap before switching from {tires[i]} to {tires[i + 1]}",
                min_value=1,
                max_value=total_laps,
                value=(i + 1) * 5
            )
            pit_laps.append(lap)

    # Start simulation button
    start_sim = st.sidebar.button("Start Simulation")

    return {
        "track": track,
        "weather": weather,
        "tires": tires,
        "fuel": fuel,
        "total_laps": total_laps,
        "strategy_mode": strategy_mode,
        "num_runs": num_runs,
        "pit_laps": pit_laps,
        "start_sim": start_sim
    }
