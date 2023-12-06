import numpy as np
from scipy import integrate
import pandas as pd
import matplotlib.pyplot as plt

def calculate_ecsa(file_path, sheet_name):
    # Load data from the Excel file
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Convert data in the first and second columns to numeric as float
    data.iloc[:, 0] = pd.to_numeric(data.iloc[:, 0], errors='coerce').astype(float)  # Assuming 'Potential' is in the first column
    data.iloc[:, 1] = pd.to_numeric(data.iloc[:, 1], errors='coerce').astype(float)  # Assuming 'Current' is in the second column

    # Drop rows with NaN values
    data = data.dropna()

    # Extract potential (E) and current (i) data
    potential = data.iloc[:, 0]  # First column (Voltage)
    current = data.iloc[:, 1]/1000  # Second column (Amps)

    return potential, current

def plot_and_calculate_ecsa(file_path, sheet_name, electrode_area, surface_load, surface_charge, integration_range):
    # Calculate ECSA for the sample
    potential, current = calculate_ecsa(file_path, sheet_name)

    # Filter data based on the specified potential range
    mask = (potential >= integration_range[0]) & (potential <= integration_range[1])
    potential_range = potential[mask]
    current_range = current[mask]

    # Plot the cyclic voltammogram with the specified integration range
    plt.figure(figsize=(8, 5))
    plt.plot(potential, current, label=f'Cyclic Voltammogram - {sheet_name}')
    plt.axvspan(min(potential_range), max(potential_range), color='red', alpha=0.3, label='Integration Range')
    plt.xlabel('Potential (V)')
    plt.ylabel('Current (A)')
    plt.title(f'Cyclic Voltammogram - {sheet_name}')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Integrate the current with respect to potential within the specified range to obtain charge (Q)
    charge = integrate.simps(current_range, potential_range) #Units of Coulomb (C)
    theta = surface_charge #Coulomb per m2
    load = surface_load
    area = electrode_area
    ECSA = charge/(theta*load*area) #centimeter squared

    return ECSA

# Example usage
file_path = 'Fuel cell lab 121222 Data.xlsx'
electrode_area = 0.0005  # Area of the platinum electrode, 5 m2
surface_load = 4  # Surface load, 4 grams per m2
surface_charge = 2.1  # Surface charge of a full proton layer on polycrystalline Pt, Coulomb/m2..

# Specify the integration range for the old sample (start and end potentials)
integration_range_old = (0, 0.5)  # Replace with the desired range

# Calculate and plot ECSA for the "old" sample
old_sample_ecsa = plot_and_calculate_ecsa(file_path, 'CV aged', electrode_area, surface_load, surface_charge, integration_range_old)

# Specify the integration range for the new sample (start and end potentials)
integration_range_new = (0, 0.5)  # Replace with the desired range

# Calculate and plot ECSA for the "new" sample
new_sample_ecsa = plot_and_calculate_ecsa(file_path, 'CV fresh', electrode_area, surface_load, surface_charge, integration_range_new)

print(f'ECSA (Old Sample): {old_sample_ecsa:.6f} m²/g')
print(f'ECSA (New Sample): {new_sample_ecsa:.6f} m²/g')