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
	fitness.write('\n')	

def Filewrite_Genome():
	gen = Population.genome
	gen = str(gen)
	genome.write(gen)
	genome.write('\n')

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
	size = 2		#Size of Population
	genome = [] 		#all the genome's of the population
	fitness = [] 		#the fitness's of all the population
	

#+++++++++++++++++INITIALISATION STUFF+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def Init_Maze():
	Maze.maze = Master_Maze	#copy the original maze into the maze class
	Maze.nmaze = numpy.array(Maze.maze) #make a numpy maze
	print "Initialised Maze"

def Init_Population():
	table = []
	i = 0
	while i in range(Population.size):
		for row in range(64): #64 bits long becasue there are 32 possible action of forward, left of right 
			table.append(random.randint(0,1))#append random value at the end of the table
		print "table ",table	
		Population.genome.append(table)
		
		i = i + 1
	
	print "Population of ", Population.size ," Initialised"
	#pp.pprint(Population.genome)	

def Init_Robot():
	Robot.x = 2 # the row
	Robot.y = 1 # the col
	Robot.heading = 1 #Start Facing East
	Robot.fitval = 0
	#Robot.brain = the current genome in the population
	print "Robot Initialised"
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def Del_Tile():
	if Maze.maze[Robot.x][Robot.y] == 1:
		Maze.maze[Robot.x][Robot.y] = 0 #if robot has passed through a tile == 1 then make it 3 to show its path

def Robot_Fitness():
	if Maze.maze[Robot.x][Robot.y] == 1: #if the robot is in a trail tile then add one to the fitness
		Robot.fitness = Robot.fitness + 1








#++++++++++++++++MAIN+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Init_Maze()
Init_Robot()
Init_Population()	

pp.pprint (Maze.maze)
print Maze.nmaze

