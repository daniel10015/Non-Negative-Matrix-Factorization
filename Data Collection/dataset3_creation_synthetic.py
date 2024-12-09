import os
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from time import time

"""
    Generate synthetic data for a single time step and save it to a CSV file.
    Returns:
    - filename (str): The filename of the saved CSV.
    """
def generate_time_data(t: int, n: int, m: int, T: int, folder: str) -> str:
    # Base data matrix with positive values
    base_data = np.random.poisson(10, (m, n))  # Poisson distribution for counts
    # Add variability over time
    trend = np.sin(2 * np.pi * t / T) * 5  # Periodic trend
    noise = np.random.normal(0, 2, (m, n))  # Small noise
    time_data = base_data + trend + noise
    time_data = np.maximum(time_data, 1)  # Ensure all values are positive

    # Convert to DataFrame
    df = pd.DataFrame(time_data, columns=[f"Feature_{i+1}" for i in range(n)])

    # Save to CSV
    filename = os.path.join(folder, f"time_{t}.csv")
    df.to_csv(filename, index=False)
    print(f"Saved timestep {t} data to {filename}")

    return filename

"""
    Generate synthetic time-series data for online NMF using multithreading to speed up the generation.

    Returns:
    - file_list (list): List of filenames generated.
    """
def generate_synthetic_data_multithreaded(n: int, m: int, T: int, folder="Data/Dataset3/", num_threads=16):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    file_list = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for each time step
        futures = [
            executor.submit(generate_time_data, t, n, m, T, folder)
            for t in range(T)
        ]

        # Collect results
        for future in futures:
            file_list.append(future.result())

    return file_list

# Parameters: n (features), m (observations), T (time points)
n, m, T = 20, 500, 100000  # Adjust values as needed
start_time = time()

generate_synthetic_data_multithreaded(n, m, T, "Data/Dataset3/", num_threads=16)

total_time = int(time() - start_time) 
print(f"----------\nTime taken: {total_time//60} minutes, {total_time%60} seconds.")
