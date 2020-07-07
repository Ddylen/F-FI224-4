"""
Code to plot graphs of the effect of filtering on the raw data in 1D
"""
import csv
import matplotlib.pyplot as plt
import numpy as np


def read_csv(csvname, keyrows):
    """Function to extract CSV files"""
    
    #Define empty list of lists to store the read data in
    savedrows = [[]]*len(keyrows)
    
    #Read data from CSV
    with open(csvname + '.csv', newline='') as csvfile:
        readfile = csv.reader(csvfile, dialect='excel')
        rownum= 1 #number of row in csv file
        savedrownum = 0 #row in savedrows that csv row is saved to
        for row in readfile:
            if rownum in keyrows:
                savedrows[savedrownum] = row
                savedrownum = savedrownum + 1
            rownum = rownum + 1
            
    return savedrows


def plot_against(filteredfilename, unfilteredfilename):
    """Function to plot two lists of filtered and unfiltered data against each other"""
    
    #Define font size
    size = 40
    plt.rcParams['axes.labelsize'] = size
    plt.rcParams['axes.titlesize'] = size
    plt.tick_params(axis='both', which='major', labelsize=size-10)
    
    #Define plot limits
    plt.xlim((700,1500))
    plt.ylim((-0.5,0.5))
    
    #Define the set of rows you want to plot
    rightwristxnum = 29
    rightwristynum = 30
    rightwristznum = 31
    rightwristlostnum = 32
    rightwristrows = [rightwristxnum, rightwristynum, rightwristznum, rightwristlostnum]
    
    #Read both the filtered and unfiltered CSV files
    filteredoutput = read_csv(filteredfilename, rightwristrows) 
    unfilteredoutput = read_csv(unfilteredfilename, rightwristrows) 
    
    #Define length of data to be plotted
    x = np.arange(len((unfilteredoutput[0][1:])))
    
    #Plot both the filtered and unfiltered data
    plt.plot(x, unfilteredoutput[0][1:], label = 'Unfiltered', color = '#C0C0C0')
    plt.plot(x, filteredoutput[0][1:], label = 'Filtered')
    
    #Define plot labels
    plt.title('Filtered vs Unfiltered Data for the X Position of the Wrist of Demonstrator D')
    plt.xlabel('Frame Number')
    plt.ylabel('Position (m)')
    plt.legend(loc = 'upper left', fontsize = size-10)
    
    
if __name__ == "__main__":
    
    plot_against('testtrial8luca.17.3.11.12filteredREDO', 'testtrial8luca.17.3.11.12REDO')