#!/usr/bin/python
from __future__ import division
#Advances in Artificial Intelligence - Coursework 1 Version 2.0

#The Artificial Neural Network

#first import the required python packages, mostly from numpy I think
import numpy #for maths
import numpy.random
import random
import array
import sys
import pprint as pp
import copy
import time
import pipes


random.seed()
numpy.set_printoptions(threshold=sys.maxint) #numpy likes to print large arrays wierd, supress this


fitness = open('./data/annfitness.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
def Filewrite_Fitness():
	fit = Robot.fitval
	fit = str(fit)	
	fitness.write (fit)
	fitness.write(' \n')	
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

#+++++++++++++MAZE CLASS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#The only thing that should happen to this is deleting the tiles as the Robot drives over them
#Try and do everything with the numpy maze, use the normal maze just for drawing stuff

class Maze: #	
	maze = []
	nmaze = []

#++++++++++++Robot CLASS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Robot:
	x = 0 			#X Position
	y = 0 			#Y position
	heading = 0 		#0 = N,  1 = E , 2 = S, 3 = W
 	format_head = 0 	#keep the display of heading separate to the actual heading, its only for show
	health = 25  		#Robot can only move 25 places so every move it looses a health point  
	fitval = 0 		#Robot Fitness
	oldfit = 0	
	sens = [0,0,0,0,0] 	#[left, leftd, fwd, rightd, right]
	dsens = 0 		#Denary Sensor Values
	cwarn = 0 		#Crash Warning Flag
	genome = []
	finflag = 0

class Neuron1:
	weight = []
	oldw = []
	val = 0
	outweight = 0
		
class Neuron2:
	weight = []
	oldfit = 0
	val = 0
	outweight = 0

class Neuron3:
	weight = []
	oldfit = 0
	val = 0
	outweight = 0 

class OutNeu1:
	weight = 0
	val = 0

class OutNeu2:
	weight = []
	val = 0
#+++++++++++++++++INITIALISATION STUFF+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#--------------INIT MAZE------------------------------------------------------------------------------------INIT MAZE
#
#copy the master maze into the numpy array and the normal array
def Init_Maze(): 
	Maze.maze = Master_Maze	#copy the original maze into the maze class
	Maze.nmaze = numpy.array(Master_Maze) #make a numpy maze
	print "Initialised Maze"

#--------------INIT Robot----------------------------------------------------------------------------------INIT ROBOT
#
#Initalise the Robot, start in the start position headin east, and load in a genome from the population
#
def Init_Robot():
	Robot.x = 2 		# The start row				N(0)
	Robot.y = 1 		# The start column			|
	Robot.heading = 1	# Start Facing East		  W(3)--0--E(1)
	Robot.fitval = 0	# Fitness				|
	#Robot.brain = the current genome in the population		S(2)
	print "Robot Initialised"

def Init_Neurons():
	#there will be 3 weights per neuron for each sensor
	#generate initial weights for the input layer
	for i in range(0,3):
		Neuron1.weight.append(random.random())
		Neuron2.weight.append(random.random())
		Neuron3.weight.append(random.random())
	print "Neuron 1",Neuron1.weight
	print "Neuron 1",Neuron2.weight
	print "Neuron 1",Neuron3.weight

	OutNeu1.weight = random.random()
	Neuron2.outweight = random.random()
	Neuron3.outweight = random.random()		


#---------------FORMAT HEADING FUNCTION----------------------------------------------------------------FORMAT HEADING FUNCTION
#
#Just easier to debug, change the heading of the Robot into something meaningful for printing
#By passing the new heading format into a new variable, saving the actual maze data
#
def Format_Heading():
	if Robot.heading == 0: #North
		Robot.format_head = '^'
	elif Robot.heading == 1: #East
		Robot.format_head = '>'
	elif Robot.heading == 2: #South
		Robot.format_head = 'v'
	elif Robot.heading == 3: #West
		Robot.format_head = '<'

#---------------DELETE TILE FUNCTION-----------------------------------------------------------------------DELETE TILE FUNCTION
#
#Check to see if the Robot is on a tile, if it is, delete the tile. if this isn't done then the Robot could 
#run over the same tile twice and count that as a fitness step, also it looks better
#
def Del_Tile():
	if Maze.nmaze[Robot.x , Robot.y] == 1:
		Maze.nmaze[Robot.x , Robot.y] = 0 #if Robot has passed through a tile == 1 then make it 3 to show its path
		Maze.maze = Maze.nmaze.tolist()	#copy the numpy maze back into the standard maze, just for drawing	
	else:
		pass #The robots probably gone through a 0, do nothing


#---------------ROBOT FITNESS FUNCTION-------------------------------------------------------------------ROBOT FITNESS FUNCTION
#
#If the Robot is on a tile then add 1 to its fitness
#
def Robot_Fitness():
	if Maze.nmaze[Robot.x , Robot.y] == 1: #if the Robot is in a trail tile then add one to the fitness		
		Robot.fitval = Robot.fitval + 1
		
	else:
		pass

#-------------GET SENSOR DATA-----------------------------------------------------------------------------GET SENSOR DATA
#
#
def Get_Sensors(): 
	x = Robot.x
	minusx = x - 1
	plusx = x + 1
	
	y = Robot.y
	minusy = y - 1
	plusy = y + 1

	MwrapX = x - 7
	PwrapX = x + 7
	MwrapY = y - 7
	PwrapY = y + 7
	
	#+++++++++++NORTH HEADING+++++++++++++++++++++++++++++++++++	
	if Robot.heading == 0: #North
		Robot.sens[0] = Maze.nmaze[x	,	minusy	]	#Left Sensor
		#Robot.sens[1] = Maze.nmaze[minusx,	minusy	]	#Left Diagonal Sensor
		Robot.sens[2] = Maze.nmaze[minusx,	y	]	#Forward Sensor
		#Robot.sens[3] = Maze.nmaze[minusx,	plusy	]	#Right Diagonal Sensor
		Robot.sens[4] = Maze.nmaze[x	,	plusy 	]	#Right Sensor Sensor
	#++++++++++EAST HEADING+++++++++++++++++++++++++++++++++++++
	elif Robot.heading == 1: # East
		Robot.sens[0] = Maze.nmaze[minusx,	y	]
		#Robot.sens[1] = Maze.nmaze[minusx,	plusy	]
		Robot.sens[2] = Maze.nmaze[x	,	plusy	]
		#Robot.sens[3] = Maze.nmaze[plusx, 	plusy	]
		Robot.sens[4] = Maze.nmaze[plusx,	y	]
	#++++++++++SOUTH HEADING+++++++++++++++++++++++++++++++++++++
	elif Robot.heading == 2: # South
		Robot.sens[0] = Maze.nmaze[x	,	plusy	]
		#Robot.sens[1] = Maze.nmaze[plusx,	plusy	]
		Robot.sens[2] = Maze.nmaze[plusx,	y	]
		#Robot.sens[3] = Maze.nmaze[plusx,	plusy	]
		Robot.sens[4] = Maze.nmaze[x	,	minusy	]
	#++++++++++WEST HEADING+++++++++++++++++++++++++++++++++++++
	elif Robot.heading == 3: #West
		Robot.sens[0] = Maze.nmaze[plusx,	y	]
		#Robot.sens[1] = Maze.nmaze[plusx,	minusy	]
		Robot.sens[2] = Maze.nmaze[x	,	minusy	]
		#Robot.sens[3] = Maze.nmaze[minusx,	minusy	]
		Robot.sens[4] = Maze.nmaze[minusx,	y	]
		
	
	#++++++++++++++++NORTH WRAPPING++++++++++++++++++++++++++++++
	if Robot.heading == 0: #north
		if Robot.sens[2] == 2: #if front is at a border 
			Robot.sens[2] = Maze.nmaze[PwrapX , y] #this was Mwrap
			Robot.cwarn = 1

		if Robot.sens[0] == 2: #if left is at border
			Robot.sens[0] = Maze.nmaze[x , PwrapY]
	
		if Robot.sens[4] == 2: #if right is at  border
			Robot.sens[4] = Maze.nmaze[x , MwrapY]
	
	#++++++++++++++++EAST WRAPPING+++++++++++++++++++++++++++++	
	elif Robot.heading == 1: #east

		if Robot.sens[2] == 2: #front
			Robot.sens[2] = Maze.nmaze[x , MwrapY]
			Robot.cwarn = 1

		if Robot.sens[0] == 2: #left is at border
			Robot.sens[0] = Maze.nmaze[PwrapX , y]

		if Robot.sens[4] == 2: #if right is at border
			Robot.sens[4] = Maze.nmaze[MwrapX , y]

	#+++++++++++++++SOUTH WRAPPING+++++++++++++++++++++++++++
	elif Robot.heading == 2: #SOUTH
		
		if Robot.sens[2] == 2:
			Robot.sens[2] = Maze.nmaze[MwrapX , y]
			Robot.cwarn = 1
	
		if Robot.sens[0] == 2:
			Robot.sens[0] = Maze.nmaze[x , MwrapY]

		if Robot.sens[4] == 2:
			Robot.sens[4] = Maze.nmaze[x , PwrapY]

	#+++++++++++++++WEST WRAPPING++++++++++++++++++++++++++
	elif Robot.heading == 3: #WEST

		if Robot.sens[2] == 2:
			Robot.sens[2] = Maze.nmaze[x , PwrapY]
			Robot.cwarn = 1

		if Robot.sens[0] == 2:
			Robot.sens[0] = Maze.nmaze[MwrapX , y]

		if Robot.sens[4] == 2:
			Robot.sens[4] = Maze.nmaze[PwrapX , y]
	

	#++++++++For now always make the diagonal sensors = 0++++++++++++++++
	Robot.sens[1] = 0
	Robot.sens[3] = 0
	
	#++++++++Convert the sensor data into a single denary value++++++++++
	dsens = 0
	x1 = 0
	for x in Robot.sens[:]:
		dsens = dsens + x * pow(2, x1)
		x1 = x1+1
	Robot.dsens = dsens #pass dsens to the Robot class
	#print "dsens in sensors ", Robot.dsens
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	
	#print "Got Sensors"

def Robot_Action(val):
	action = val
	if action == 0:
		print "Action called - Do Nothing"	
	elif action == 1:
		print "Action called - Turn Right"
	elif action == 2:
		print "Action called - Turn Left"
	elif action == 3:
		print "Action called - Go Forward"
	
	#now we have an action selected, drive the robot
	#+++++++++++++++++STATE MACHINE ACTION SELECTOR++++++++++++++++++++++++++++++++++++++++++++
	if action == 0:
		Robot.cwarn = 0 #do nothing
	elif action == 1: #Turn Right
		Robot.cwarn = 0 #now that you've turned reset the crash flag
		if Robot.heading == 0: 			#Heading at North, make your heading East
			Robot.heading = 1	
		elif Robot.heading == 1: 		#heading at East, make your heading South						
			Robot.heading = 2 			
		elif Robot.heading == 2: 		#heading at South, make your heading West
			Robot.heading = 3
		elif Robot.heading == 3: 		#heading at West, make your heading North
			Robot.heading = 0			
	elif action == 2: #Turn Left
		Robot.cwarn = 0 #now that you've turned reset the crash flag
		if Robot.heading == 0: 			#Heading at North, make your heading West
			Robot.heading = 3
		elif Robot.heading == 1: 		#Heading at East, make your heading North
			Robot.heading = 0
		elif Robot.heading == 2: 		#Heading at South, make your heading East
			Robot.heading = 1
		elif Robot.heading == 3:		#Heading at West, make your heading South
			Robot.heading = 2

	elif action == 3: #Go Forward 
		if Robot.heading == 0: #heading north
			if Robot.cwarn == 1: #crash warning raised
				#print "wrapping robot at X Co-ord", Robot.x
				Robot.x = Robot.x + 7 #your at a border dont drive into that, so wrap to top of maze
				#time.sleep(5)				
				Robot.cwarn = 0 #reset crash flag
			elif Robot.cwarn == 0: #was just an else 
				Robot.x = Robot.x - 1						     

		elif Robot.heading == 1: #heading east								
			if Robot.cwarn == 1:
				#print "wrapping robot at X Co-ord", Robot.x
				Robot.y = Robot.y - 7
				#time.sleep(5)
				Robot.cwarn = 0			
			elif Robot.cwarn == 0: #was just an else
				Robot.y = Robot.y + 1							
		
		elif Robot.heading == 2: #heading south
			if Robot.cwarn == 1:
				#print "wrapping robot at X Co-ord", Robot.x
				Robot.x = Robot.x - 7
				#time.sleep(5)				
				Robot.cwarn = 0							
			elif Robot.cwarn == 0: #was just an else
				Robot.x = Robot.x + 1		
							
		elif Robot.heading == 3: #heading west
			if Robot.cwarn == 1:
				#print "wrapping robot at X Co-ord", Robot.x
				#time.sleep(5)				
				Robot.cwarn = 0
				Robot.y = Robot.y + 7							
			elif Robot.cwarn == 0: #was just an else
				Robot.y = Robot.y - 1
		
		Robot_Fitness()	
		Robot.cwarn = 0
		Del_Tile()#delete the tile your on so you dont count its fitness more than once

#------------------Neural Network--------------------------------------------------------------------NEURAL NETWORK
#
#
#
def ANN():
	for life in range(Robot.health):
		Get_Sensors()
		Neuron1.val = (Robot.sens[0] * Neuron1.weight[0]) + (Robot.sens[2] * Neuron1.weight[1]) + (Robot.sens[4] * Neuron1.weight[2])
		Neuron2.val = (Robot.sens[0] * Neuron2.weight[0]) + (Robot.sens[2] * Neuron2.weight[1]) + (Robot.sens[4] * Neuron2.weight[2])
		Neuron3.val = (Robot.sens[0] * Neuron3.weight[0]) + (Robot.sens[2] * Neuron3.weight[1]) + (Robot.sens[4] * Neuron3.weight[2])
	
		print"1 = ", Neuron1.val
		print"2 = ", Neuron2.val
		print"3 = ", Neuron3.val
	
		#if a neuron is over the firerate then output its value to the output neurons
	
		OutNeu1.val = (Neuron1.val * OutNeu1.weight) + (Neuron2.val * OutNeu1.weight) + (Neuron3.val * OutNeu1.weight)
		OutNeu2.val = (Neuron1.val * OutNeu2.weight) + (Neuron2.val * OutNeu2.weight) + (Neuron3.val * OutNeu2.weight)
	
		# if the value of the output neuron is above the firerate then normalise to 1 or 0 and output to drive
	
	
		if OutNeu1.val > 1:
			OutNeu1.val = 1
		elif OutNeu1.val < 1:
			OutNeu1.val = 0
	
		if OutNeu2.val > 1:
			OutNeu2.val = 1
		if OutNeu2.val < 1:
			OutNeu2.val = 0
	
		if OutNeu1.val == 0 and OutNeu2.val == 0:
			Robot_Action(0)
			Format_Heading()
		elif OutNeu1.val == 0 and OutNeu2.val == 1:
			Robot_Action(1)
			Format_Heading()
		elif OutNeu1.val == 1 and OutNeu2.val == 0:
			Robot_Action(2)
			Format_Heading()
		elif OutNeu1.val == 1 and OutNeu2.val == 1:
			Robot_Action(3)
			Format_Heading()
	
		maze2 = copy.deepcopy(Maze.maze) #this is just for formating
		maze2[Robot.x][Robot.y] = Robot.format_head #format heading
		pp.pprint(maze2)
		print "Robot Fitness ", Robot.fitval
		time.sleep(0)
		Filewrite_Fitness()
		
	if Robot.fitval == 19:
		Robot.finflag = 1
	else:
		Robot.finflag = 0

def Mutation(val):
	a = 0
	b = random.randint(0,1)
	if b == 0:
		a = random.random()
		a = a/10
		outval = val + a
	elif b == 1:
		a = random.random()
		a = a * -1
		a = a/10
		outval = val + a 
		


	return outval
#------------------------MAIN----------------------------------------------------------------------MAIN
Init_Maze()
Init_Robot()
Init_Neurons()
count = 0
while Robot.finflag == 0:
	Init_Maze()
	Init_Robot()	
	ANN()
	Robot.oldfit = Robot.fitval
	Neuron1.oldw = Neuron1.weight
	Neuron2.oldw = Neuron2.weight
	Neuron3.oldw = Neuron3.weight
	if Robot.oldfit > Robot.fitval:
		#old fitness is better throw out the new weights, they suck
		Neuron1.weight = Neuron1.oldw
		Neuron2.weight = Neuron2.oldw
		Neuron3.weight = Neuron3.oldw

	elif Robot.fitval < Robot.oldfit:
		pass	#keep the new weights, they rule
	
	#Mutation
	for i in range(0,3):
		print "mutating"
		print "val" , Neuron1.weight[i]
		Neuron1.weight[i] = Mutation(Neuron1.weight[i])
		print "outval" , Neuron1.weight[i]
	
	count = count + 1
	if count == 1000:
		print "current fitness ", Robot.fitval
		print "old fitness", Robot.oldfit
		count = 0
		time.sleep(10)










