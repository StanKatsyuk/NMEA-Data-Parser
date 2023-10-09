import matplotlib.pyplot as plt
from typing import Optional
from utils.logger import Logger


class DataPlotter:
    def __init__(self):
        self.timestamps = []
        self.satellites_tracked = []
        self.satellites_in_view = []
        self.logger = Logger(__name__)

    def add_data_point(self, timestamp, tracked, in_view):
        self.timestamps.append(timestamp)
        self.satellites_tracked.append(tracked)
        self.satellites_in_view.append(in_view)

    def plot_data(self, data: list[tuple[float, str, int]], ttff: Optional[float]):
        if not data:
            self.logger.error("No data available to plot.")
            return

        timestamps = []
        satellites_in_view = []
        satellites_tracked = []

        for timestamp, sat_type, count in data:
            timestamps.append(timestamp)
            if sat_type == "in_view":
                satellites_in_view.append(count)
                satellites_tracked.append(None)  # Placeholder for tracked satellites
            else:
                satellites_tracked.append(count)
                satellites_in_view.append(None)  # Placeholder for satellites in view

        # Move the plotting section outside the loop
        plt.plot(timestamps, satellites_in_view, label="Satellites in View", marker="o")
        plt.plot(timestamps, satellites_tracked, label="Satellites Tracked", marker="x")

        if ttff:
            # Adding a space marker to create a legend entry for TTFF
            plt.plot(
                [], [], " ", label=f"TTFF: {ttff} seconds", marker="o", color="white"
            )  # White marker for legend

        plt.xlabel("Timestamp")
        plt.ylabel("Number of Satellites")
        plt.title("Satellites in View vs. Satellites Tracked")
        plt.legend()
        plt.grid(True)
        plt.show()
