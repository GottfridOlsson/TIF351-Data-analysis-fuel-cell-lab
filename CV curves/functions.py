##=============================================##
##     Project: PLOT DATA
##        File: functions.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-06-21, 17:50
##     Updated: 2022-08-02, 15:40
##       About: Helper functions for plotting.
##=============================================##

import matplotlib


def cm_2_inch(cm):
    return cm/2.54


def set_LaTeX_and_CMU(LaTeX_and_CMU_on=True):
    if LaTeX_and_CMU_on:
        matplotlib.rcParams.update({
    "text.usetex": True,
    "font.family": "serif", 
    "font.serif" : ["Computer Modern Roman"]
    })
    print("DONE: set_LaTeX_and_CMU: " + str(LaTeX_and_CMU_on))


def set_font_size(axis=13, tick=11, legend=9): #2023-05-27, set standard values
    matplotlib.rc('font',   size=axis)      #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('axes',   titlesize=axis) #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('axes',   labelsize=axis) #2022-06-21: not sure what the difference is, to test later on!
    matplotlib.rc('xtick',  labelsize=tick)
    matplotlib.rc('ytick',  labelsize=tick)
    matplotlib.rc('legend', fontsize=legend)
    print("DONE: set_font_size: (axis, tick, legend): " + str(axis) + ", " + str(tick) + ", " + str(legend))


def set_title(title):
    matplotlib.pyplot.title(title)
    print("DONE: set_title to: " + str(title))

def set_axis_labels(ax, x_label, y_label, axNum=None):
    ax.set_xlabel(str(x_label))
    ax.set_ylabel(str(y_label))
    print("DONE: set_axis_labels: on axs: " + str(axNum))


def set_legend(ax, legend_on, alpha, location, axNum=None):
            
    if legend_on:
        ax.legend(framealpha=alpha, loc=location)
    print("DONE: set_legend: (on, alpha, location): " + str(legend_on) + ", " + str(alpha) + ", " + str(location) + ", on axs: " + str(axNum))


def set_grid(ax, grid_major_on, grid_major_linewidth, grid_minor_on, grid_minor_linewidth, axNum=None):
    if grid_major_on:
        ax.grid(grid_major_on, which='major', linewidth=grid_major_linewidth) 
    if grid_minor_on:
        ax.minorticks_on()
        ax.grid(grid_minor_on, which='minor', linewidth=grid_minor_linewidth)
    ###ax.grid(True, which='both', linewidth=grid_minor_linewidth) # TEMP 2023-02-23, did NOT put logarithmic grids on my linear-log plot (x-y)
    print("DONE: set_grid: grid_major: " + str(grid_major_on) +", grid_minor: "+ str(grid_minor_on)+  " on axs: " + str(axNum))


def set_axis_scale(ax, xScale_string, yScale_string, axNum=None):
    ax.set_xscale(xScale_string)
    ax.set_yscale(yScale_string)
    print("DONE: set_axis_scale: X: " + str(xScale_string) + ", Y: " + str(yScale_string) + " on axs: " + str(axNum))


def set_axis_limits(ax, xmin, xmax, ymin, ymax, axNum=None):
    if not xmin: xmin = None
    if not xmax: xmax = None
    if not ymin: ymin = None
    if not ymax: ymax = None
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    print("DONE: set_axis_limits: x=(" + str(xmin) + ", " + str(xmax)+ ") and y=(" + str(ymin) + ", " + str(ymax)+ ") on axs: " + str(axNum))


def set_axis_invert(ax, x_invert, y_invert, axNum=None):
    if x_invert: ax.invert_xaxis()
    if y_invert: ax.invert_yaxis()
    print("DONE: set_axis_invert: x: " + str(x_invert) + ", y: " + str(y_invert) + " on axs: " + str(axNum))


def set_commaDecimal_with_precision_x_axis(ax, xAxis_precision, axNum=None):
    xFormatString = '{:.' + str(xAxis_precision) + 'f}'
    ax.get_xaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: xFormatString.format(x).replace('.', ',')) )    
    print("DONE: set_commaDecimal_with_precision_x_axis: "+str(xAxis_precision) + " on axs: "+str(axNum))

def set_commaDecimal_with_precision_y_axis(ax, yAxis_precision, axNum=None):
    yFormatString = '{:.' + str(yAxis_precision) + 'f}'
    ax.get_yaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: yFormatString.format(x).replace('.', ',')) )    
    print("DONE: set_commaDecimal_with_precision_y_axis: "+str(yAxis_precision) + " on axs: "+str(axNum))


def set_pointDecimal_with_precision_x_axis(ax, xAxis_precision, axNum=None):
    xFormatString = '{:.' + str(xAxis_precision) + 'f}'
    ax.get_xaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: xFormatString.format(x)) )    
    print("DONE: set_pointDecimal_with_precision_x_axis: "+str(xAxis_precision) + " on axs: "+str(axNum))

def set_pointDecimal_with_precision_y_axis(ax, yAxis_precision, axNum=None):
    yFormatString = '{:.' + str(yAxis_precision) + 'f}'
    ax.get_yaxis().set_major_formatter( matplotlib.ticker.FuncFormatter(lambda x, pos: yFormatString.format(x)) )    
    print("DONE: set_pointDecimal_with_precision_y_axis: "+str(yAxis_precision) + " on axs: "+str(axNum))


def set_layout_tight(fig):
    fig.tight_layout()
    print("DONE: set_layout_tight")


def align_labels(fig):
    fig.align_labels()
    print("DONE: align_labels")
    

def export_figure_as_pdf(filePath):
    matplotlib.pyplot.savefig(filePath, format='pdf', bbox_inches='tight')#, metadata={"Author" : "Gottfrid Olsson", "Title" : "", "Keywords" : "Created with PlotData by Gottfrid Olsson"}) ##this could be implemented in the future, 2022-06-21
    print("DONE: export_figure_as_pdf: " + filePath)
