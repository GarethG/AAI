#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1

#first import the required python packages, mostly from numpy I think
import numpy #can be used with matlab?
import random
import sys

numpy.set_printoptions(threshold=sys.maxint) #numpy like to print large arrays wierd, supress this


#specify the population size and the genome size - do this later with raw_input
pop = 50 #population
gen = 10 #number of bits or genome size


def populate_matrix(rows, cols):

    seq = [int(i) for i in range(int(0), int(2))]
    matrix = []

    for row in range(rows):
        array = []
        for col in range(cols):
            array.append(random.choice(seq))
        matrix.append(array)

    return matrix



a = populate_matrix(pop,gen)
b = numpy.array(a)
numpy.set_printoptions(threshold=sys.maxint)
print b


