##======================================================================##
##     Project: [TIF351] FUEL CELL LAB - DATA ANALYSIS
##        File: Polarization curve plotting.py
##      Author: GOTTFRID OLSSON 
##     Created: 2023-12-06
##     Updated: 2023-12-06
##       About: Plot data from CSV with matplotlib.
##              1. Read CSV
##              2. Do calculations (change this dependent on your case).
##              3. Plot x_data and y_data, change any settings you want.
##======================================================================##


# LIBRARIES #
import CSV_handler as CSV
import functions as f
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as plticker

# READ CSV #
# Change these:
filename_csv = 'TIF351_Fuel-cell-laboration_polarization-curve-data.csv' 
filename_pdf = 'TIF351_Fuel-cell-laboration_polarization-curves.pdf'

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_path = CURRENT_PATH + "\\" + filename_csv # "\\CSV\\" +
PDF_path = CURRENT_PATH + "\\" + filename_pdf # "\\PDF\\" +

CSV_data   = CSV.read(CSV_path)
CSV_header = CSV.get_header(CSV_data)


# Select data
x_data_fresh = CSV_data[CSV_header[0]]
y_data_fresh = CSV_data[CSV_header[1]]

x_data_aged = CSV_data[CSV_header[2]]
y_data_aged = CSV_data[CSV_header[3]]


# DATA ANLYSIS / CALCULATIONS #
A = 5 # cm^2
x_data_fresh = -x_data_fresh / A #convert from current to current density and flip sign
x_data_aged = -x_data_aged / A


# PLOT SETTINGS #
x_lim = [-25, 900] #[np.min(x_data_aged), np.max(x_data_aged)]
y_lim = [0.45, 1.05] #[np.min(y_data_aged), np.max(y_data_aged)]

f.set_LaTeX_and_CMU(True) #must be before plotting
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(16/2.54, 9/2.54), sharex=False, sharey=False)


# Plot
axs.plot(x_data_fresh, y_data_fresh, linewidth=1.5, linestyle='', color='b', marker='.', markersize='1', label='Fresh sample')
axs.plot(x_data_aged,  y_data_aged,  linewidth=1.5, linestyle='', color='r', marker='.', markersize='1', label='Aged sample')
#axs.errorbar(763.8, 21.9, 1.5, label='Unknown concentration', color='r', capsize=2.5, marker='')

# Settings for each axis
f.set_font_size(axis=13, tick=11, legend=9)
f.set_axis_scale(   axs, xScale_string='linear', yScale_string='linear')
f.set_axis_labels(  axs, x_label="Current density / $\\rm mA\,cm^{-2}$", y_label="Potential / $\mathrm{V}_{\mathrm{RHE}}$")
f.set_axis_invert(  axs, x_invert=False, y_invert=False)
f.set_axis_limits(  axs, x_lim[0], x_lim[1], y_lim[0], y_lim[1])
f.set_grid(         axs, grid_major_on=True, grid_major_linewidth=0.7, grid_minor_on=False, grid_minor_linewidth=0.3) # set_grid must be after set_axis_scale for some reason (at least with 'log')
f.set_legend(       axs, legend_on=True, alpha=1.0, location='best')


#loc = plticker.MultipleLocator(base=5) # this locator puts ticks at regular intervals
#axs.xaxis.set_major_locator(loc)

f.align_labels(fig)
f.set_layout_tight(fig)
f.export_figure_as_pdf(PDF_path)
plt.show()