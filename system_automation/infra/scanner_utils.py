import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List



def plot_graph(data: List[float]):
    # Applying a moving average filter with window size 3
    smoothed_data = np.convolve(data, np.ones(3) / 3, mode='valid')

    # Plot the original and smoothed data
    plt.plot(range(len(smoothed_data)), smoothed_data, label='Smoothed Data')
    plt.plot(range(len(data)), data, 'o-', label='Original Data')

    # Add labels and title
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Plot of Array of Floats')

    # Add legend
    plt.legend()

    # Show the plot
    plt.show()


def turn_position_to_degree(data: List[float]) -> List[float]:
    """
    Converts raw mirror positions to degrees.

    Args:
    data (list): List of raw mirror positions.

    Returns:
    list: List of mirror positions in degrees.
    """
    # The magic number (2 ** 24) represents the maximum value of the mirror position.
    # It is used to scale the positions to a range of 0 to 360 degrees.
    return [(pos / (2 ** 24)) * 360 for pos in data]


def calculate_differential(mirror_degree):
    dt = 100e-6  # seconds
    timestamp = np.arange(1, len(mirror_degree) + 1) * dt  # Timestamp calculation

    # Calculate time difference between consecutive measurements
    mirror_time_diff = np.diff(timestamp)

    # Calculate mirror velocity
    mirror_vel = np.diff(mirror_degree) / mirror_time_diff
    return mirror_vel


def make_continuous(mirror_degree):
    """
    Adjusts mirror positions to keep them within a continuous range.

    Args:
    mirror_degree (list): List of mirror positions in degrees.

    Returns:
    list: List of adjusted mirror positions.
    """
    pos_discontinuity_constant = 200
    adjusted_positions = [pos - 360 if pos > pos_discontinuity_constant else pos for pos in mirror_degree]
    plot_graph(adjusted_positions)
    return adjusted_positions


def get_peak_degree(raw_data: List[float]) -> float:
    """
    Calculates the peak degree from raw data.

    Args:
    raw_data (list): List of raw data.

    Returns:
    float: Peak degree.
    """
    deg_arr = turn_position_to_degree(raw_data)
    cont_arr = make_continuous(deg_arr)

    # Find the maximum absolute degree value in the continuous array
    peak_degree = max(abs(max(cont_arr)), abs(min(cont_arr)))

    return peak_degree

