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

#bf = open('./data/bestfit.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
#mf = open('./data/meanfit.txt','a')


#+++++++++++++++++++++MAZE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
maze =  [
	[ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
	[ 0 , 1 , 1 , 1 , 1 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ],
	[ 0 , 2 , 1 , 1 , 0 , 0 , 0 , 1 ],
	[ 0 , 0 , 0 , 1 , 1 , 1 , 1 , 1 ],
	[ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
	]

nmaze = numpy.array(maze)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++ROBOT CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class robot:
	x = 0
	y = 0
	heading = 0 #0 = N,  1 = E , 2 = S, 3 = W
 
	health = 0  #robot can only move 25 places so every move it looses a health point  
	
	sens = [0,0,0,0,0] #[left, leftd, fwd, rightd, right]
 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++init robot++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_init():
	robot.x = 2 # the row
	robot.y = 2 # the col
	robot.heading = 0
	print "Robot Initialised"

#+++++++++++++++++++++++++++++++++MOVE ROBOT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_move(xpos, ypos, robheading):
	robot.x = xpos
	robot.y = ypos
	robot.heading = robheading

#++++++++++++++++++++++++++++++++GET SENSORS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_getsensors(xpos, ypos, robheading):
	#robot.sens[1] = 
	print "getting sensors"
	print "heading ", robot.heading

	x = robot.x
	minusx = robot.x - 1
	plusx = robot.x + 1
	
	y = robot.y
	minusy = robot.y - 1
	plusy = robot.y + 1
	
	#+++++++++++NORTH HEADING+++++++++++++++++++++++++++++++++++
	if robot.heading == 0: #North
		robot.sens[0] = nmaze[x,	minusy	]
		robot.sens[1] = nmaze[minusx,	minusy	]
		robot.sens[2] = nmaze[minusx,	y	]
		robot.sens[3] = nmaze[minusx,	plusy	]
		robot.sens[4] = nmaze[x,	plusy 	]
	#++++++++++EAST HEADING+++++++++++++++++++++++++++++++++++++
	if robot.heading == 1: # East
		robot.sens[0] = nmaze[minusx,	y	]
		robot.sens[1] = nmaze[minusx,	plusy	]
		robot.sens[2] = nmaze[x,	plusy	]
		robot.sens[3] = nmaze[plusx, 	plusy	]
		robot.sens[4] = nmaze[plusx,	y	]
	#++++++++++SOUTH HEADING+++++++++++++++++++++++++++++++++++++
	if robot.heading == 2: # South
		robot.sens[0] = nmaze[x,	plusy	]
		robot.sens[1] = nmaze[plusx,	plusy	]
		robot.sens[2] = nmaze[plusx,	y	]
		robot.sens[3] = nmaze[plusx,	plusy	]
		robot.sens[4] = nmaze[x,	minusy	]
	#++++++++++WEST HEADING+++++++++++++++++++++++++++++++++++++
	if robot.heading == 2: #West
		robot.sens[0] = nmaze[plusx,	y	]
		robot.sens[1] = nmaze[plusx,	minusy	]
		robot.sens[2] = nmaze[x,	minusy	]
		robot.sens[3] = nmaze[minusx,	minusy	]
		robot.sens[4] = nmaze[minusx,	y	]

print "Create Maze"
pp.pprint(maze)

print "The Numpy Maze"
print nmaze

#robot.x = 4

robot_init() #initialise the robot

robot_getsensors(0,1,0)
#+++++++++++++++++++++++++++workout the sensors++++++++++++++++++++++++++++++++++

#a = nmaze[robot.y,robot.x]
#print a
#+++++++++++++++++++++++++++++++++++++++++++++++
#print "Move through the maze"

#a  = maze[]
#print "I'm trying to get all of the A's out of my body", a


#for row in nmaze:
#	for col in row:
#		robot.y = nmaze
#		print robot.y
#	robot.x = col
#	print robot.x


	
