# -*- coding: utf-8 -*-
"""
Created on Mon May 11 18:20:26 2020

@author: birl
"""
import csv

import matplotlib.pyplot as plt
import numpy as np

size = 40
plt.rcParams['axes.labelsize'] = size
plt.rcParams['axes.titlesize'] = size



filteredfilename = 'testtrial8luca.17.3.11.12filteredREDO'

unfilteredfilename = 'testtrial8luca.17.3.11.12REDO'



rightwristxnum = 29
rightwristynum = 30
rightwristznum = 31
rightwristlostnum = 32

rightwristrows = [rightwristxnum, rightwristynum, rightwristznum, rightwristlostnum]


def read_csv(csvname, keyrows):
    savedrows = [[]]*len(keyrows)
    
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


filteredoutput = read_csv(filteredfilename, rightwristrows) 
unfilteredoutput = read_csv(unfilteredfilename, rightwristrows) 

plt.tick_params(axis='both', which='major', labelsize=size-10)


x = np.arange(len((unfilteredoutput[0][1:])))


plt.xlim((0,3050))
plt.ylim((-0.5,0.5))
plt.plot(x, unfilteredoutput[0][1:], label = 'Unfiltered', color = '#C0C0C0')
plt.plot(x, filteredoutput[0][1:], label = 'Filtered')




plt.title('Filtered vs Unfiltered Data for the X Position of the Wrist of Demonstrator D')
plt.xlabel('Frame Number')
plt.ylabel('Position (m)')
plt.legend(loc = 'upper left', fontsize = size-10)