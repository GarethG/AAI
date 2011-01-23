#!/usr/bin/python

#Advances in Artificial Intelligence - Coursework 1

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

#bf = open('./data/bestfit.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
#mf = open('./data/meanfit.txt','a')


#+++++++++++++++++++++MAZE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
maze =  [
	[ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
	[ 0 , 1 , 1 , 1 , 1 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 0 , 0 ],
	[ 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1 ],
	[ 0 , 1 , 1 , 1 , 0 , 0 , 0 , 1 ],
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
	robot.x = 1 # the row
	robot.y = 0 # the col
	robot.heading = 1 #Start Facing East
	print "Robot Initialised"

#+++++++++++++++++++++++++++++++++MOVE ROBOT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_move(xpos, ypos, robheading):
	robot.x = xpos
	robot.y = ypos
	robot.heading = robheading

#++++++++++++++++++++++++++++++++GET SENSORS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_getsensors(xpos, ypos, robheading):
	
	print "Getting Sensors"

	x = xpos
	minusx = xpos - 1
	plusx = xpos + 1
	
	y = ypos
	minusy = ypos - 1
	plusy = ypos + 1

	#if the robot reaches the end of the maze it's sensors should wrap around so
	#check to see if robot is at a border of a maze
	if robot.x == 0:
		minusx = 7
	if robot.x == 7:
		plusx = 0
	if robot.y == 0:
		minusy = 7		
	if robot.y == 7:
		plusy = 0	

	#+++++++++++NORTH HEADING+++++++++++++++++++++++++++++++++++	
	if robot.heading == 0: #North
		robot.sens[0] = nmaze[x,	minusy	]	#Left Sensor
		robot.sens[1] = nmaze[minusx,	minusy	]	#Left Diagonal Sensor
		robot.sens[2] = nmaze[minusx,	y	]	#Forward Sensor
		robot.sens[3] = nmaze[minusx,	plusy	]	#Right Diagonal Sensor
		robot.sens[4] = nmaze[x,	plusy 	]	#Right Sensor Sensor
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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++LINE FOLLOWER++++++++++++++++++++++++++++++++++++++++++++++++
def line_follow():
	if robot.x == 0:
		robot.x = 7
	if robot.x == 7:
		robot.x = 0
	if robot.y == 0:
		robot.y = 7		
	if robot.y == 7:
		robot.y = 0	

	#++++++++++++++++TURN LEFT+++++++++++++++++++++++++++++++++++++++++++++++++++++++
	if robot.sens[0] == 1: #Turn Left
		if robot.heading == 0: 		#Heading at North, make your heading West
			robot.heading = 3
		elif robot.heading == 1: 		#Heading at East, make your heading North
			robot.heading = 0
		elif robot.heading == 2: 		#Heading at South, make your heading East
			robot.heading = 1
		elif robot.heading == 3:		#Heading at West, make your heading South
			robot.heading = 2
	
	#+++++++++++++++TURN RIGHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++
	elif robot.sens[4] == 1:
		if robot.heading == 0: 		#Heading at North, make your heading East
			robot.heading = 1	
		elif robot.heading == 1: 		#heading at East, make your heading South						
			robot.heading = 2 			
		elif robot.heading == 2: 		#heading at South, make your heading West
			robot.heading = 3
		elif robot.heading == 3: 		#heading at West, make your heading North
			robot.heading = 0			
		
	#+++++++++++++++FORWARD++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	elif robot.sens[2] == 1:	
		if robot.heading == 0: #heading north
			robot.x = robot.x + 1
		elif robot.heading == 1: #heading east
			robot.y = robot.y + 1
			print "move forward"
		elif robot.heading == 2: #heading south
			robot.x = robot.x - 1
			
		elif robot.heading == 3: #heading west
			robot.y = robot.y - 1

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def format_heading():
	if robot.heading == 0:
		rhead = '^'
	if robot.heading == 1:
		rhead = '>'
	if robot.heading == 2:
		rhead = 'v'
	if robot.heading == 3:
		rhead = '<'
	print "rhead ", rhead
	return rhead

def draw_map():
	pass

print "Create Maze"
pp.pprint(maze)

print "The Numpy Maze"
print nmaze

#robot.x = 4

robot_init() #initialise the robot

print "Getting first position"
robot_getsensors(robot.x,robot.y,robot.heading)

lifetime = 25
for life in range(lifetime):
	line_follow()
	robot_getsensors(robot.x,robot.y,robot.heading)
	print "Iteration ", life
	print "Sensors ", robot.sens
	print "Heading" , robot.heading
	print "robot x pos ", robot.x
	print "robot y pos ", robot.y
	maze2 = copy.deepcopy(maze)
	rhead = 0
	format_heading()
	maze2[robot.x][robot.y] = rhead
	pp.pprint(maze2)
	time.sleep(1)
	
print"check the old maze is still intact"
pp.pprint(maze)

#maze2[2][2] = 'R'
#pp.pprint (maze2)

#draw_map()


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


	
