#!/usr/bin/python

from pylab import *
import time
import pipes

#--------------SETUP THE PIPES--------------------------------
# shouldnt need any of this as im just reading in this script
#t = pipes.Template()
#t.append('tr a-z A-Z', '--')
#f = t.open('/tmp/fsmfitness','w')
#f.close()

fitness  = 0

#t = arange(0.0, 2.0, 0.01)
#s = sin(2*pi*t)
#plot(t, s, linewidth=1.0)

xlabel('Generation')
ylabel('Fitness')
title('Rolling Fitness')
grid(True)


print "Reading in from the Pipes"
fitness = open('/tmp/fsmfitness').read()
generation = open('/tmp/fsmgeneration').read()
if generation == '':
	while generation != '':
		generation = open('/tmp/fsmgeneration').read()

print "Converting from String to Ints"
fitness = int(fitness)
generation = int(generation)

print "Plotting"
plot( generation, fitness,linewidth=1.0)
show() #use draw instead

	
iteration = 0
while fitness < 19:
	print "begin loop"
	print "Reading in from the Pipes"
	fitness = open('/tmp/fsmfitness').read()
	generation = open('/tmp/fsmgeneration').read()
	if generation == '':
		while generation != '':
			generation = open('/tmp/fsmgeneration').read()

	print "Converting from String to Ints"
	fitness = int(fitness)
	generation = int(generation)
	print "Iteration ", iteration
	iteration = iteration + 1
	print "Plotting"
	plot( generation, fitness,linewidth=1.0)
	draw() #use draw instead
	time.sleep(5)
	
