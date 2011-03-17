#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1 Version 2.0

#The Finite State Machine

#first import the required python packages, mostly from numpy I think
import numpy #can be used with matlab?
import numpy.random
import random
import array
import sys
import pprint as pp
import copy
import time

numpy.set_printoptions(threshold=sys.maxint) #numpy likes to print large arrays wierd, supress this

#+++++++++++++++++++++File input args+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
fitness = open('./data/fitness.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
genome = open('./data/genome.txt','a')

#++++++++++++++++WRITE TO FILE+++++++++++++++++++++++++++++++++++++++++++++++++++
def Filewrite_Fitness():
	fit = Robot.fitness
	fit = str(fit)	
	fitness.write (fit)
	fitness.write(' \n')	

def Filewrite_Genome(): #write the whole genome to a file
	for i in range(Population.size):
		gen = Population.genome[i]
		gen = str(gen)
		genome.write(gen)
		genome.write(' \n')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++ ORIGINAL MAZE - DONT WRITE TO THIS++++++++++++++++++++++++++++++++++++++++++++++++++
Master_Maze =  [
	[ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],
	[ 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 ],
	[ 2 , 0 , 1 , 1 , 1 , 1 , 1 , 0 , 0 , 2 ],
	[ 2 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 2 ],
	[ 2 , 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 , 2 ],
	[ 2 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 , 2 ],
	[ 2 , 0 , 1 , 1 , 1 , 0 , 0 , 0 , 1 , 2 ],
	[ 2 , 0 , 0 , 0 , 1 , 1 , 1 , 1 , 1 , 2 ],
	[ 2 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 2 ],
	[ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],
	]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++MAZE CLASS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#The only thing that should happen to this is deleting the tiles as the robot drives over them
#Try and do everything with the numpy maze, use the normal maze just for drawing stuff

class Maze: #	
	maze = []
	nmaze = []

#++++++++++++ROBOT CLASS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Robot:
	x = 0 			#X Position
	y = 0 			#Y position
	heading = 0 		#0 = N,  1 = E , 2 = S, 3 = W
 	format_head = 0 	#keep the display of heading separate to the actual heading, its only for show
	health = 26  		#robot can only move 25 places so every move it looses a health point  
	fitval = 0 		#Robot Fitness
	sens = [0,0,0,0,0] 	#[left, leftd, fwd, rightd, right]
	dsens = 0 		#Denary Sensor Values
	cwarn = 0 		#Crash Warning Flag
	brain = []

	

#++++++++++POPULATION CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Population:
	size = 10		#Size of Population
	genome = [] 		#all the genome's of the population
	genlen = 64		#length of the genome	
	fitness = [] 		#the fitness's of all the population
	

#+++++++++++++++++INITIALISATION STUFF+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------INIT MAZE-----------------------------------------------------------------------
#
#copy the master maze into the numpy array and the normal array
def Init_Maze(): 
	Maze.maze = Master_Maze	#copy the original maze into the maze class
	Maze.nmaze = numpy.array(Master_Maze) #make a numpy maze
	print "Initialised Maze"

#--------------INIT ROBOT----------------------------------------------------------------------
#
#Initalise the robot, start in the start position headin east, and load in a genome from the population
#
def Init_Robot():
	Robot.x = 2 		# The row				N(0)
	Robot.y = 1 		# The column				|
	Robot.heading = 1 	# Start Facing East		  W(3)--0--E(1)
	Robot.fitval = 0	# Fitness				|
	#Robot.brain = the current genome in the population		S(2)
	print "Robot Initialised"

#------------INIT POPULATION--------------------------------------------------------------------
#
#Initialise the population, create N number (specified by Population.size) of genome's n bits long
#
def Init_Population():
	table = []
	i = 0
	
	for i in range(Population.size): #in range of the size of the population
		Population.genome.append(Gen_Genome(Population.genlen))	#append a genome at the end of the genome stack, genlen = length of genome
		i = i + 1
		
	print "Population of ", Population.size ," Initialised" #use len() to make this more accurate
	Filewrite_Genome()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#---------------FORMAT HEADING FUNCTION----------------------------------------------------------------
#
#Just easier to debug, change the heading of the robot into something meaningful for printing
#By passing the new heading format into a new variable, saving the actual maze data
#
def Format_Heading():
	if Robot.heading == 0: #North
		Robot.mhead = '^'
	elif Robot.heading == 1: #East
		Robot.mhead = '>'
	elif Robot.heading == 2: #South
		Robot.mhead = 'v'
	elif Robot.heading == 3: #West
		Robot.mhead = '<'

#---------------DELETE TILE FUNCTION-------------------------------------------------------------------
#
#Check to see if the robot is on a tile, if it is, delete the tile. if this isn't done then the robot could 
#run over the same tile twice and count that as a fitness step, also it looks better
#
def Del_Tile():
	if Maze.maze[Robot.x][Robot.y] == 1:
		Maze.maze[Robot.x][Robot.y] = 0 #if robot has passed through a tile == 1 then make it 3 to show its path

#---------------ROBOT FITNESS FUNCTION-------------------------------------------------------------------
#
#If the robot is on a tile then add 1 to its fitness
#
def Robot_Fitness():
	if Maze.maze[Robot.x][Robot.y] == 1: #if the robot is in a trail tile then add one to the fitness
		Robot.fitness = Robot.fitness + 1


#--------------GENERATE GENOME FUNCTION-------------------------------------------------------------------
#
#Generate a binary bit pattern of a specified size
#
def Gen_Genome(size): 
	table = []
	for row in range(size): #size is passed in from the call
		table.append(random.randint(0,1))#append random value at the end of table
	return table #return a single bit pattern, size large


def Get_Sensors(x,y,th): #pass in the robots x, y and theta(heading)
	pass


#++++++++++++++++MAIN+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Init_Maze()
Init_Robot()
Init_Population()	

i = 0
for i in range (Population.size):
	print "Genome Number", i, "is ", len(Population.genome[i]), "bits long"	
	print Population.genome[i]
	i = i + 1

#pp.pprint (Maze.maze)
#print Maze.nmaze

