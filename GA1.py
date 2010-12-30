#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1

#first import the required python packages, mostly from numpy I think
import numpy #can be used with matlab?
import numpy.random
import random
import sys

numpy.set_printoptions(threshold=sys.maxint) #numpy likes to print large arrays wierd, supress this


#specify the population size and the genome size - do this later with raw_input
pop = 5 #population
gen = 5 #number of bits or genome size
fitval = []
totfit = 0 #total fitness used in roulette wheel selection
a = 0
b= 0

def pop_array(rows, cols):

	seq = [int(i) for i in range(int(0), int(2))]
	matrix = []

	for row in range(rows):
		array = []
		for col in range(cols):
			array.append(random.choice(seq))	
		matrix.append(array)
		fit = array.count(1)
		fitval.append(fit)
		
		
	return matrix
	
	

a = pop_array(pop,gen)# function call to create an array and populate it
b = numpy.array(a) #convert the python list array to a numpy array - probably just for printing
totfit = b.sum() # total fitness of the population

print "Initial Population created"
print b


#print b[49,:] how to print one line of an array
#sum the indexed array element
print "the total fitness of the population is = ",totfit

row =0

for row in b:
	#numpy.append(fitarr, b[1,row].sum())
	print "in ", row, " the fitness is ",b[1,row]

	
	

