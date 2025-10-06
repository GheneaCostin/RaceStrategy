import streamlit as st
from visualization.dashboard import sidebar_controls
from simulation.race_environment import RaceEnvironment
from visualization.plots import plot_lap_times, plot_tire_wear, plot_fuel


def main():
    st.title(" Race Strategy AI Dashboard")

    controls = sidebar_controls()

    if controls["start_sim"]:
        total_laps = controls["total_laps"]
        track = controls["track"]
        tires = controls["tires"] or ["Soft"]
        fuel = controls["fuel"]
        weather = controls["weather"]

        race = RaceEnvironment(
            total_laps=total_laps,
            initial_fuel=fuel,
            track=track,
            tire_compound=tires[0],
            weather=weather
        )

        # Determine pit strategy
        pit_strategy = controls["pit_laps"] if controls["strategy_mode"] == "Manual" else [total_laps // 2]

        # Multiple simulation runs
        all_runs = []
        for run in range(controls["num_runs"]):
            race.reset()
            result = race.simulate_race(pit_strategy=pit_strategy, tire_stints=tires)
            all_runs.append(result)

        # Average lap times
        avg_lap_times = [sum(lap) / len(lap) for lap in zip(*[r["lap_times"] for r in all_runs])]
        avg_total_race_time = sum(avg_lap_times) + sum(
            [sum([race.get_pit_stop_time() for _ in r["pit_stops"]]) for r in all_runs]) / len(all_runs)

        st.subheader("Simulation Results")
        st.write("Average Lap Times:", avg_lap_times)
        st.write("Average Total Race Time (including pit stops):", round(avg_total_race_time, 2), "seconds")
        st.write("Pit Stops (last run example):", all_runs[-1]["pit_stops"])
        st.write("Tire History (last run example):", all_runs[-1]["tire_history"])
        st.write("Fuel History (last run example):", all_runs[-1]["fuel_history"])

        # Lap times chart
        st.subheader("Lap Times")
        st.plotly_chart(plot_lap_times(all_runs[-1]["lap_times"], pit_stops=all_runs[-1]["pit_stops"]))

        # Tire wear chart
        st.subheader("Tire Wear")
        st.plotly_chart(plot_tire_wear(all_runs[-1]["tire_history"], pit_stops=all_runs[-1]["pit_stops"]))

        # Fuel chart
        st.subheader("Fuel Level")
        st.plotly_chart(plot_fuel(all_runs[-1]["fuel_history"], pit_stops=all_runs[-1]["pit_stops"]))


if __name__ == "__main__":
    main()