#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1

#first import the required python packages, mostly from numpy I think
import numpy #can be used with matlab?
import numpy.random
import random
import array
import sys
import pprint as pp

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


pp.pprint(a)

print a[0,0]

print "Initial Population created"
print b


#print b[49,:] how to print one line of an array
#sum the indexed array element
print "the total fitness of the population is = ",totfit

print "array element 0,0 is ", b[0,0]

y = b[0,:]
print y

#for row in b:
#	for col in b:
#		print b[row,col]
#		u = u + b[row,col]
#	print "test total fitness for b", u
#	u = 0


	
	

