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

#+++++++++++++++++++++File input args+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=

bf = open('./data/bestfit.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
mf = open('./data/meanfit.txt','a')

#specify the population size and the genome size - do this later with raw_input
pop = 10 #population
gen = 10 #number of bits or genome size
fitval = []
totfit = 0 #total fitness used in roulette wheel selection
meanfit = 0
a = 0
b= 0
randparent = []
randind = 0
randfit = 0


def pop_array(rows, cols):

	matrix = []

	for row in range(rows):
		array = []
		for col in range(cols):
			array.append(random.randint(0,1))	
		matrix.append(array)
		
		
	return matrix
#################################################################	
def write_bestfit(topfit):
	#write best fitness of current population to file
	bfval = str(topfit)
	bf.write(bfval)
	bf.write('\n')	
#################################################################

#################################################################
def write_meanfit(fitnessval):
	#write mean fitness of current population to file
	meanfit = sum(fitnessval, 0.0) / len(fitnessval)
	mfval = str(meanfit)
	mf.write(mfval)
	mf.write('\n')	
################################################################

#####################################################################################################################

def roulette(totfit):
	randfit = random.randint(0 , totfit) #choose a random fitness between 0 and the fitness of the population
	randparent = []
	randind = 0

	resum = 0
	for row in a:
		randind = randind + 1 # find the index of the element where you stop
		resum = resum + row.count(1)
		if resum > randfit:
			print "randfit reached"
			randparent = row 
		 
			break
	print "randfit, randparent and totfit are in function = ", randfit, randparent, totfit
	return randparent, randfit, randind
	print "fitness of all genes ",fitval 
	print "ENTERED"
#####################################################################################################################


a = pop_array(pop,gen)# function call to create an array and populate it
b = numpy.array(a) #convert the python list array to a numpy array - probably just for printing
print  b.sum() # total fitness of the population

print "Initial Population created"

#print a
pp.pprint(a)

#print a[0],[0]
#print a[1],[1]
#j = a[0].count(1)
#print j
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#					FITNESS CALCULATIONS
for row in a:
	fitval.append(row.count(1))

totfit = sum(fitval) #find the total fitness of the population
topfit = max(fitval) #find the highest fitness in the fitness list
write_bestfit(topfit) #write the highest fitness found to file
write_meanfit(fitval) #write the mean fitness of the current population to a file
topfitx = fitval.count(topfit) #take the highest fitness value and count the number of times it appears in the list


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#					ROULETTE WHEEL SELECTION
print "calling roulette wheel selection"
r = roulette(totfit)
randparent = r[0]
randfit = r[1]
randind = r[2]
#now need to create a new array of new parents


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print "the total fitness of the population is = ",totfit
print "the highest fitness of ", topfit, " Occurs ", topfitx, " times"


print "-----------------------------------------------------------------"
print"-		Roulette Wheel Selection Stuff			-"
print "- 								-"
print "- Total fitness of the population = ", totfit, "			-"
print "-								-"
print "- A random number between 0 and total fitness = ", randfit, "		-"	
print "-								-"
print "- 								-"
print "-----------------------------------------------------------------"


print "the random parents are", randparent
print "the index of that parent is ", randind


#End of Line
bf.close() #close these files
mf.close()

#print b[49,:] how to print one line of an array
#sum the indexed array element



#for row in b:
#	for col in b:
#		print b[row,col]
#		u = u + b[row,col]
#	print "test total fitness for b", u
#	u = 0


	
	

