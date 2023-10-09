import matplotlib.pyplot as plt
from typing import Optional
from utils.logger import Logger

logger = Logger(__name__)


class DataPlotter:
    def plot_data(self, timestamps: list[float], satellite_counts: list[int], ttff: Optional[float]):
        """
        Plot the data showing the number of satellites tracked as a function of time.

        Args:
            timestamps (List[float]): List of timestamps (in seconds).
            satellite_counts (List[int]): List of the number of satellites tracked at each timestamp.

        Returns:
            None
        """
        logger.info(f'Will attempt to plot {timestamps=}, {satellite_counts=}, {ttff=}')

        # Plot the data and assign labels
        plt.plot(timestamps, satellite_counts, '-o', label='Satellites Tracked')
        if ttff is not None:
            plt.axvline(ttff, color='red', linestyle='--', label='Time to First Fix (TTFF)')

        plt.xlabel('Time (seconds)')
        plt.ylabel('Number of Satellites')
        plt.title('Satellites Tracked vs Time')
        plt.grid(True)
        
        # Create a legend
        plt.legend()
        
        # Show the plot
        plt.show()

    def plot_ttff(self, ttff: float):
        plt.axvline(x=ttff, color='r', linestyle='--', label=f'TTFF: {ttff} s')
        plt.xlabel('Time (seconds)')
        plt.title('Time to First Fix (TTFF)')
        plt.grid(True)
        plt.legend()
        plt.show()
