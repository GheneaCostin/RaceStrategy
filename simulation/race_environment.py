import random

TIRE_COMPOUNDS = {
    "Soft": {"wear_rate": 0.015},
    "Medium": {"wear_rate": 0.01},
    "Hard": {"wear_rate": 0.005},
}

TRACKS = {
    "Monaco": {"base_lap": 78, "tire_wear_factor": 1.2, "fuel_factor": 1.0},
    "Silverstone": {"base_lap": 90, "tire_wear_factor": 1.0, "fuel_factor": 1.0},
    "Spa": {"base_lap": 92, "tire_wear_factor": 1.1, "fuel_factor": 1.0},
    "Monza": {"base_lap": 85, "tire_wear_factor": 0.9, "fuel_factor": 1.0},
    "Barcelona": {"base_lap": 95, "tire_wear_factor": 1.1, "fuel_factor": 1.0},
}

WEATHER = {
    "Sunny": {"lap_factor": 1.0, "tire_wear_factor": 1.0},
    "Rain": {"lap_factor": 1.05, "tire_wear_factor": 1.2},
    "Variable": {"lap_factor": 1.02, "tire_wear_factor": 1.1},
}

BASE_PIT_STOP_TIME = 22  # seconds

class RaceEnvironment:
    def __init__(self, total_laps=20, initial_fuel=100, track="Monaco", tire_compound="Soft", weather="Sunny"):
        self.total_laps = total_laps
        self.initial_fuel = initial_fuel
        self.fuel = initial_fuel
        self.track = track
        self.tire_compound = tire_compound
        self.tire_params = TIRE_COMPOUNDS[tire_compound]
        self.tire_condition = 1.0
        self.weather = weather
        self.track_params = TRACKS[track]
        self.weather_params = WEATHER[weather]
        self.lap_times = []
        self.tire_history = []
        self.fuel_history = []
        self.pit_stops = []
        self.lap = 0
        self.fuel_consumption = initial_fuel

    def reset(self):
        """Reset all race variables for multiple runs"""
        self.fuel = self.initial_fuel
        self.tire_condition = 1.0
        self.lap_times = []
        self.tire_history = []
        self.fuel_history = []
        self.pit_stops = []
        self.lap = 0

    def simulate_lap(self):
        """Simulate a single lap with small random noise"""
        lap_factor = self.weather_params["lap_factor"]
        tire_wear_factor = self.weather_params["tire_wear_factor"]
        base_lap_time = self.track_params["base_lap"]

        lap_time = base_lap_time * (
            1
            + (1 - self.tire_condition) * 0.5 * self.track_params["tire_wear_factor"] * tire_wear_factor
            + (self.fuel / 100) * 0.02 * self.track_params["fuel_factor"]
        ) * lap_factor

        # Add small random noise ±0.5%
        noise = random.uniform(-0.005, 0.005) * lap_time
        lap_time += noise

        # Record history
        self.lap_times.append(lap_time)
        self.tire_history.append(self.tire_condition)
        self.fuel_history.append(self.fuel)

        # Update tire and fuel
        self.tire_condition -= self.tire_params["wear_rate"] * tire_wear_factor
        self.tire_condition = max(self.tire_condition, 0)
        self.fuel -= self.fuel_consumption / self.total_laps
        self.fuel = max(self.fuel, 0)
        self.lap += 1

        return lap_time

    def pit_stop(self):
        """Simulate a pit stop: reset tires and refuel"""
        self.tire_condition = 1.0
        self.fuel = self.initial_fuel
        self.pit_stops.append(self.lap)

    def get_pit_stop_time(self):
        """Return pit stop time with small random variability ±1 second"""
        return BASE_PIT_STOP_TIME + random.uniform(-1, 1)

    def simulate_race(self, pit_strategy=[], tire_stints=None):
        """Simulate full race with optional pit strategy and tire stints"""
        if tire_stints is None:
            tire_stints = [self.tire_compound]

        current_stint = 0
        self.tire_compound = tire_stints[current_stint]
        self.tire_params = TIRE_COMPOUNDS[self.tire_compound]

        total_pit_time = 0

        for lap in range(1, self.total_laps + 1):
            self.simulate_lap()

            if lap in pit_strategy:
                self.pit_stop()
                pit_time = self.get_pit_stop_time()
                total_pit_time += pit_time

                # Move to next tire compound if any
                if current_stint + 1 < len(tire_stints):
                    current_stint += 1
                    self.tire_compound = tire_stints[current_stint]
                    self.tire_params = TIRE_COMPOUNDS[self.tire_compound]

        total_race_time = sum(self.lap_times) + total_pit_time

        return {
            "lap_times": self.lap_times,
            "tire_history": self.tire_history,
            "fuel_history": self.fuel_history,
            "pit_stops": self.pit_stops,
            "total_race_time": total_race_time
        }