#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1

#first import the required python packages, mostly from numpy I think
import numpy #can be used with matlab?
import random
import sys

numpy.set_printoptions(threshold=sys.maxint) #numpy likes to print large arrays wierd, supress this


#specify the population size and the genome size - do this later with raw_input
pop = 50 #population
gen = 10 #number of bits or genome size
fitval = []

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
c = fitval.index(10) + 1 #zero referenced


print "Initial Population created"
print b
print fitval
print "the index of 10 fitval genes", c


