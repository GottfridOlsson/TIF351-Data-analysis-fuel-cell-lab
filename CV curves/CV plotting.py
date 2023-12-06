##======================================================================##
##     Project: [TIF351] FUEL CELL LAB - DATA ANALYSIS
##        File: CS plotting.py
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
filename_csv = 'TIF351_Fuel-cell-laboration_CV-curve-data.csv' 
filename_pdf = 'TIF351_Fuel-cell-laboration_CV-curves.pdf'

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_path = CURRENT_PATH + "\\CSV\\" + filename_csv
PDF_path = CURRENT_PATH + "\\PDF\\" + filename_pdf

CSV_data   = CSV.read(CSV_path)
CSV_header = CSV.get_header(CSV_data)



# FUNCTIONS #

concentrations = [0, 5, 10, 20, 30, 50] # percent glycol in water (zero means only water, values from lab)
LSPR_peak_time_ranges = [(70,130), (240,300), (395,455), (545,605), (700,760), (810,870), (1050,1110)] # corresponding times for concentrations (values from plot)
LSPR_peak_means = []

# DATA ANLYSIS / CALCULATIONS #


# Select data
x_data = CSV_data[CSV_header[0]]
y_data = CSV_data[CSV_header[1]]
LSPR_peaks = x_data
concentrations = y_data
fit_x = CSV_data[CSV_header[2]]
fit_y = CSV_data[CSV_header[3]]
fit_y_oneSigma = CSV_data[CSV_header[4]]


# PLOT SETTINGS #
x_lim = [761.6,766.8] #[np.min(x_data), np.max(x_data)]
y_lim = [0,55] #[np.min(y_data), np.max(y_data)]

f.set_LaTeX_and_CMU(True) #must be before plotting
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(16/2.54, 9/2.54), sharex=False, sharey=False)


# Plot
axs.plot(x_data, y_data, linewidth=1.5, linestyle='', color='k', marker='o', markersize='4.5', label='Measured data')
axs.plot(fit_x, fit_y, color='k', linestyle='-', label='Linear fit')
axs.fill_between(fit_x, fit_y + 2*fit_y_oneSigma, fit_y - 2*fit_y_oneSigma, color='b', alpha=0.25, label=f'Prediction interval ($2\\sigma$)')
#axs.errorbar(763.8, 21.9, 1.5, label='Unknown concentration', color='r', capsize=2.5, marker='')

# Settings for each axis
f.set_font_size(axis=13, tick=11, legend=9)
f.set_axis_scale(   axs, xScale_string='linear', yScale_string='linear')
f.set_axis_labels(  axs, x_label="LSPR peak wavelength / nm", y_label="Concentration (\%)")
f.set_axis_invert(  axs, x_invert=False, y_invert=False)
f.set_axis_limits(  axs, x_lim[0], x_lim[1], y_lim[0], y_lim[1])
f.set_grid(         axs, grid_major_on=False, grid_major_linewidth=0.7, grid_minor_on=False, grid_minor_linewidth=0.3) # set_grid must be after set_axis_scale for some reason (at least with 'log')
f.set_legend(       axs, legend_on=True, alpha=1.0, location='best')


#loc = plticker.MultipleLocator(base=5) # this locator puts ticks at regular intervals
#axs.xaxis.set_major_locator(loc)

f.align_labels(fig)
f.set_layout_tight(fig)
f.export_figure_as_pdf(PDF_path)
plt.show()