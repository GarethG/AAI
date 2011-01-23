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
fitness = open('./data/fitness.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
#mf = open('./data/meanfit.txt','a')

#+++++++++++++++++++++++GLOBAL++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#fsmtable = [] #Finite State Machine Table  

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
 	mhead = 0 #keep the display of heading separate to the actual heading, its only for show
	health = 26  #robot can only move 25 places so every move it looses a health point  
	fitness = 0
	sens = [0,0,0,0,0] #[left, leftd, fwd, rightd, right]
	dsens = 0
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++FINITE STATE MACHINE CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++
class fsm:
	table = []
	action = 0
	bintable = []
#++++++++++++++++++++++init robot++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_init():
	robot.x = 1 # the row
	robot.y = 0 # the col
	robot.heading = 1 #Start Facing East
	robot.fitness = 0
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
	elif robot.x == 7:
		plusx = 0
	elif robot.y == 0:
		minusy = 7		
	elif robot.y == 7:
		plusy = 0	

	#+++++++++++NORTH HEADING+++++++++++++++++++++++++++++++++++	
	if robot.heading == 0: #North
		robot.sens[0] = nmaze[x,	minusy	]	#Left Sensor
		robot.sens[1] = nmaze[minusx,	minusy	]	#Left Diagonal Sensor
		robot.sens[2] = nmaze[minusx,	y	]	#Forward Sensor
		robot.sens[3] = nmaze[minusx,	plusy	]	#Right Diagonal Sensor
		robot.sens[4] = nmaze[x,	plusy 	]	#Right Sensor Sensor
	#++++++++++EAST HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 1: # East
		robot.sens[0] = nmaze[minusx,	y	]
		robot.sens[1] = nmaze[minusx,	plusy	]
		robot.sens[2] = nmaze[x,	plusy	]
		robot.sens[3] = nmaze[plusx, 	plusy	]
		robot.sens[4] = nmaze[plusx,	y	]
	#++++++++++SOUTH HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 2: # South
		robot.sens[0] = nmaze[x,	plusy	]
		robot.sens[1] = nmaze[plusx,	plusy	]
		robot.sens[2] = nmaze[plusx,	y	]
		robot.sens[3] = nmaze[plusx,	plusy	]
		robot.sens[4] = nmaze[x,	minusy	]
	#++++++++++WEST HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 3: #West
		robot.sens[0] = nmaze[plusx,	y	]
		robot.sens[1] = nmaze[plusx,	minusy	]
		robot.sens[2] = nmaze[x,	minusy	]
		robot.sens[3] = nmaze[minusx,	minusy	]
		robot.sens[4] = nmaze[minusx,	y	]

	#++++++++Convert the sensor data into a single denary value++++++++++
	dsens = 0
	x1 = 0
	for x in robot.sens[:]:
		dsens = dsens + x * pow(2, x1)
		x1 = x1+1
	robot.dsens = dsens #pass dsens to the robot class
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	
	

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#+++++++++++++++++++++++++LINE FOLLOWER FUNCTION FUNCTIONS++++++++++++++++++++++++++++++++
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

#++++++++++++++++++line_follow+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# decide which orientation to turn to relative to the left, forward and right sensors
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def line_follow():

	#+++++++++++++++FORWARD++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	if robot.sens[2] == 1:								#	N	
		if robot.heading == 0: #heading north					#	|
			robot.x = robot.x - 1						#    W--0--E 
		elif robot.heading == 1: #heading east					#	|		
			robot.y = robot.y + 1						#	S
		elif robot.heading == 2: #heading south					#		
			robot.x = robot.x + 1						#			
		elif robot.heading == 3: #heading west							
			robot.y = robot.y - 1
		
	#++++++++++++++++TURN LEFT+++++++++++++++++++++++++++++++++++++++++++++++++++++++
	elif robot.sens[0] == 1: #Turn Left
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
	robot_getsensors(robot.x,robot.y,robot.heading) #get sensor data
	robot_fitness() #eval the fitness of the robot
	del_tile() #remove the tile robot is currently in

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def robot_linefollow(): 
	for life in range(robot.health):
		print"------------------------------------------------------------------------"	
		print "Iteration ", life	
		line_follow()	
		#robot_getsensors(robot.x,robot.y,robot.heading)
		
		#+++++printing stuff+++++++++++++++++++++++++++++++++++++++++++++++++++++
		format_heading()#change the heading from 1 to 4 to arrows showing heading
		print "Sensors ", robot.sens
		print "Heading" , robot.mhead, " ",robot.heading
		print "robot x pos ", robot.x
		print "robot y pos ", robot.y
		maze2 = copy.deepcopy(maze)
		maze2[robot.x][robot.y] = robot.mhead
		pp.pprint(maze2)
		
		
		print"------------------------------------------------------------------------"
		time.sleep(0.2)#+++++++wait++++++++

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#----------------------END OF LINE FOLLOWER---------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

#+++++++++++++++++++FITNESS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_fitness():
	if maze[robot.x][robot.y] == 1: #if the robot is in a trail tile then add one to the fitness
		robot.fitness = robot.fitness + 1

	
#+++++++++++++++++++FORMAT HEADING+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def format_heading():
	if robot.heading == 0: #North
		robot.mhead = '^'
	elif robot.heading == 1: #East
		robot.mhead = '>'
	elif robot.heading == 2: #South
		robot.mhead = 'v'
	elif robot.heading == 3: #West
		robot.mhead = '<'
	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

#+++++++++++++++++++DELETE TILE BEHIND++++++++++++++++++++++++++++++++++++++++++++++++++++
def del_tile():
	if maze[robot.x][robot.y] == 1:
		maze[robot.x][robot.y] = 0 #if robot has passed through a tile == 1 then make it 3 to show its path

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++little animation if the robot dies+++++++++++++++++++++++++++++++++++
def robot_die():
	print "You are the weakest link goodbye"
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++little animation if the robot finds the finish+++++++++++++++++++++++
def robot_finished():
	if robot.x == 5:
		if robot.y == 1:
			print "ROBOT REACHED THE FINISH!!?!"
	elif robot.x != 5:
		if robot.y != 1:		
			robot_die()#robot must be dead
	
#++++++++++++++++WRITE FITNESS TO FILE+++++++++++++++++++++++++++++++++++++++++++++++++++
def filewrite_fitness():
	fit = robot.fitness
	fit = str(fit)	
	fitness.write (fit)
	fitness.write('\n')	





#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#+++++++++++++++++++++++++FINITE STATE MACHINE FUNCTIONS++++++++++++++++++++++++++++++++++
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#	1. Build a table with all possible sensor readings
#	2. Generate random actions for each set of sensor readings
#	3. Simulate each action and evaluate it fitness
#	4. 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-------------------------BUILD SENSOR TABLE----------------------------------------------
#-----------------------------------------------------------------------------------------
# Build a table that contains all the possible sensor readings, there are 32 possible 	--
# combinations for the 5 sensors on the robot						--
#-----------------------------------------------------------------------------------------
def fsm_build_table():
	pass
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fsm_gen_actions():
	table = []
	for row in range(32): #32 because thats the maximum number of possible sensor readings
		table.append(random.randint(0,3))#append random value at the end of fsmtable
	fsm.table = table
	
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++STATE MACHINE ACTION SELECTOR++++++++++++++++++++++++++++++++++++++++++++
def fsm_action():
	if fsm.action == 0:
		pass
	if fsm.action == 1: #Turn Right
		if robot.heading == 0: 		#Heading at North, make your heading East
			robot.heading = 1	
		elif robot.heading == 1: 		#heading at East, make your heading South						
			robot.heading = 2 			
		elif robot.heading == 2: 		#heading at South, make your heading West
			robot.heading = 3
		elif robot.heading == 3: 		#heading at West, make your heading North
			robot.heading = 0			
	if fsm.action == 2: #Turn Left
		if robot.heading == 0: 		#Heading at North, make your heading West
			robot.heading = 3
		elif robot.heading == 1: 		#Heading at East, make your heading North
			robot.heading = 0
		elif robot.heading == 2: 		#Heading at South, make your heading East
			robot.heading = 1
		elif robot.heading == 3:		#Heading at West, make your heading South
			robot.heading = 2
	if fsm.action == 3: #Go Forward 
		if robot.heading == 0: #heading north						
			robot.x = robot.x - 1						     
		elif robot.heading == 1: #heading east								
			robot.y = robot.y + 1							
		elif robot.heading == 2: #heading south							
			robot.x = robot.x + 1									
		elif robot.heading == 3: #heading west							
			robot.y = robot.y - 1
	robot_fitness()	
	del_tile()#deletethe tile your on so you dont count its fitness more than once
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++CREATE BINARY LIST+++++++++++++++++++++++++++++++++++++++++++++++
def fsm_create_binstr():
	tab = []
	bintab = []

	for row in range(32):
		tab = fsm.table[row]	
		bintab.append(bin(tab)[2:].zfill(2))#zfill is 5 to pad out bit pattern
		fsm.bintab = bintab
	
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++FSM SIMULATION+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fsm_sim():
	robot_init()
	action = 0
	for life in range(robot.health):
		print"-------------------------------------------------------------------"
		print "Iteration ", life
		robot_getsensors(robot.x,robot.y,robot.heading)
		fsm.action = fsm.table[robot.dsens]
		fsm_action()
		format_heading()
		maze2 = copy.deepcopy(maze)
		maze2[robot.x][robot.y] = robot.mhead
		pp.pprint(maze2)
		print "robot.dsens = ", robot.dsens
		print "selected action ", fsm.action
		print"-------------------------------------------------------------------"
		time.sleep(0)#+++++++wait++++++++
	
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def fsm_evolution():
	pass
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++ALL FSM IN ONE FINAL CALL+++++++++++++++++++++++++++++++++++++++++++++
def finite_state_machine():
	fsm_gen_actions()	
	fsm_sim()
	fsm_create_binstr()
	print fsm.table
	print fsm.bintab
	pyth
	#print help(fsm.bintab)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++MAIN++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print "Create Maze"
pp.pprint(maze)

print "The Numpy Maze"
print nmaze


robot_init() #initialise the robot
#robot_linefollow()
finite_state_machine()


print "robot fitness", robot.fitness
#filewrite_fitness()
#Robot has come out of its life cycle	
robot_finished() #Check to see if the robot has reached the finish

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++END OF LINE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	
##print"check the old maze is still intact"
##pp.pprint(maze)

#maze2[2][2] = 'R' How to access a single element in the array 



	
