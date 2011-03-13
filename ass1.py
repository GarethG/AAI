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
genome = open('./data/genome.txt','a')

#+++++++++++++++++++++++GLOBAL++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#fsmtable = [] #Finite State Machine Table  

#+++++++++++++++++++++MAZE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class maze:
	maze = 0
	nmaze = 0 
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
	CWarn = 0
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++FINITE STATE MACHINE CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++
class fsm:
	table = []
	action = 0
	bintable = []
	mutrate = 30
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++POPULATION CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class population:
	size = 10 #size of the population
	pop = [] #this should hold the entire population, but in the binary string of 64
	pfit = [] #rather than doing one 2D array just have another 1D array of fitness thats the same length as the population

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++init maze++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def maze_init():
	maze.maze =  [
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

	maze.nmaze = numpy.array(maze.maze)


#++++++++++++++++++++++init robot++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def robot_init():
	robot.x = 2 # the row
	robot.y = 1 # the col
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
	#if robot.x == 0:
	#	minusx = 7
	#	print "wrapping 1"
	#elif robot.x == 7:
	#	plusx = 0
	#	print "wrapping 2"
	#elif robot.y == 0:
	#	minusy = 7
	#	print "wrapping 3"
	#elif robot.y == 7:
	#	plusy = 0	
	#	print "wrapping 4"

	
	#+++++++++++NORTH HEADING+++++++++++++++++++++++++++++++++++	
	if robot.heading == 0: #North
		robot.sens[0] = maze.nmaze[x	,	minusy	]	#Left Sensor
		robot.sens[1] = maze.nmaze[minusx,	minusy	]	#Left Diagonal Sensor
		robot.sens[2] = maze.nmaze[minusx,	y	]	#Forward Sensor
		robot.sens[3] = maze.nmaze[minusx,	plusy	]	#Right Diagonal Sensor
		robot.sens[4] = maze.nmaze[x	,	plusy 	]	#Right Sensor Sensor
	#++++++++++EAST HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 1: # East
		robot.sens[0] = maze.nmaze[minusx,	y	]
		robot.sens[1] = maze.nmaze[minusx,	plusy	]
		robot.sens[2] = maze.nmaze[x	,	plusy	]
		robot.sens[3] = maze.nmaze[plusx, 	plusy	]
		robot.sens[4] = maze.nmaze[plusx,	y	]
	#++++++++++SOUTH HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 2: # South
		robot.sens[0] = maze.nmaze[x	,	plusy	]
		robot.sens[1] = maze.nmaze[plusx,	plusy	]
		robot.sens[2] = maze.nmaze[plusx,	y	]
		robot.sens[3] = maze.nmaze[plusx,	plusy	]
		robot.sens[4] = maze.nmaze[x	,	minusy	]
	#++++++++++WEST HEADING+++++++++++++++++++++++++++++++++++++
	elif robot.heading == 3: #West
		robot.sens[0] = maze.nmaze[plusx,	y	]
		robot.sens[1] = maze.nmaze[plusx,	minusy	]
		robot.sens[2] = maze.nmaze[x	,	minusy	]
		robot.sens[3] = maze.nmaze[minusx,	minusy	]
		robot.sens[4] = maze.nmaze[minusx,	y	]

	

		
	MwrapX = xpos - 7
	PwrapX = xpos + 7
	MwrapY = ypos - 7
	PwrapY = ypos + 7
	#++++++++++++++++NORTH WRAPPING++++++++++++++++++++++++++++++
	if robot.heading == 0: #north
		if robot.sens[2] == 2: #if front is at a border 
			robot.sens[2] = maze.nmaze[MwrapX , y]
			robot.CWarn = 1
			print"north 2 in front"

		if robot.sens[0] == 2: #if left is at border
			robot.sens[0] = maze.nmaze[x , PwrapY]
	
		if robot.sens[4] == 2: #if right is at  border
			robot.sens[4] = maze.nmaze[x , MwrapY]
	
	#++++++++++++++++EAST WRAPPING+++++++++++++++++++++++++++++	
	if robot.heading == 1: #east

		if robot.sens[2] == 2: #front
			robot.sens[2] = maze.nmaze[x , MwrapY]
			robot.CWarn = 1
			print"east 2 in front"

		if robot.sens[0] == 2: #left is at border
			robot.sens[0] = maze.nmaze[PwrapX , y]

		if robot.sens[4] == 2: #if right is at border
			robot.sens[4] = maze.nmaze[MwrapX , y]

	#+++++++++++++++SOUTH WRAPPING+++++++++++++++++++++++++++
	if robot.heading == 2: #SOUTH
		
		if robot.sens[2] == 2:
			robot.sens[2] = maze.nmaze[MwrapX , y]
			robot.CWarn = 1
			print"south 2 in front"
		if robot.sens[0] == 2:
			robot.sens[0] = maze.nmaze[x , MwrapY]

		if robot.sens[4] == 2:
			robot.sens[4] = maze.nmaze[x , PwrapY]

	#+++++++++++++++WEST WRAPPING++++++++++++++++++++++++++
	if robot.heading == 3: #WEST

		if robot.sens[2] == 2:
			robot.sens[2] = maze.nmaze[x , PwrapY]
			robot.CWarn = 1
			print"west 2 in front"
		if robot.sens[0] == 2:
			robot.sens[0] = maze.nmaze[MwrapX , y]

		if robot.sens[4] == 2:
			robot.sens[4] = maze.nmaze[PwrapX , y]
	

	#++++++++For now always make the diagonal sensors = 0++++++++++++++++
	robot.sens[1] = 0
	robot.sens[3] = 0
	#++++++++Convert the sensor data into a single denary value++++++++++
	dsens = 0
	x1 = 0
	for x in robot.sens[:]:
		dsens = dsens + x * pow(2, x1)
		x1 = x1+1
	robot.dsens = dsens #pass dsens to the robot class
	#print "dsens in sensors ", robot.dsens
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
	if maze.maze[robot.x][robot.y] == 1: #if the robot is in a trail tile then add one to the fitness
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
	if maze.maze[robot.x][robot.y] == 1:
		maze.maze[robot.x][robot.y] = 0 #if robot has passed through a tile == 1 then make it 3 to show its path

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

def filewrite_genome():
	gen = fsm.table
	gen = str(gen)
	genome.write(gen)
	genome.write('\n')
	





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
#+++++++++++++++++GENERATE FSM ACTIONS TABLE++++++++++++++++++++++++++++++++++++++++++++++++++++
def fsm_gen_actions(): #initialise a table for the fsm actions
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
			if robot.CWarn == 1: #crash warning raised
				robot.x = robot.x + 7 #your at a border dont drive into that so wrap to top of maze
				robot.CWarn = 0 #reset crash flag
			else: 
				robot.x = robot.x - 1						     

		elif robot.heading == 1: #heading east								
			if robot.CWarn == 1:
				robot.y = robot.y - 7
				robot.CWarn = 0			
			else:
				robot.y = robot.y + 1							
		
		elif robot.heading == 2: #heading south
			if robot.CWarn == 1:
				robot.x = robot.x - 7
				robot.CWarn = 0							
			else:
				robot.x = robot.x + 1		
							
		elif robot.heading == 3: #heading west
			if robot.CWarn == 1:
				robot.CWarn = 0
				robot.y = robot.y + 7							
			else:
				robot.y = robot.y - 1
	robot.CWarn = 0
	robot_fitness()	
	del_tile()#deletethe tile your on so you dont count its fitness more than once
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++CREATE BINARY LIST+++++++++++++++++++++++++++++++++++++++++++++++
def fsm_create_binstr():
	tab = []
	bintab = []
	newlist = []

	for row in range(32):
		tab = fsm.table[row]	
		bintab.append(bin(tab)[2:].zfill(2))#zfill is 5 to pad out bit pattern
		
	
	for row in bintab:
		if row == '00': #element = 0 so append 2 zeros
			newlist.append(0)
			newlist.append(0)
		elif row == '01': #if the element = 01 then split it and append it in a new list
			newlist.append(0)
			newlist.append(1)
		elif row == '10':
			newlist.append(1)
			newlist.append(0)
		elif row == '11':
			newlist.append(1)
			newlist.append(1)
	
	fsm.bintab = newlist
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++binary to denary++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fsm_bin2str():
	bslist = []
	j = 0
	k = 0
	bitab = fsm.bintab
	length = len(bitab)
	for k in range(0,length,2):
		j = k + 2
		if bitab[k:j] == [0,0]:
			bslist.append(0) # or 00

		elif bitab[k:j] == [0,1]:
			bslist.append(1) # or 01
			
		elif bitab[k:j] == [1,0]:
			bslist.append(2) # or 10
			
		elif bitab[k:j] == [1,1]:
			bslist.append(3) # or 11
			
		
	fsm.table = bslist #pass the new action list into the fsm table

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++MUTATION++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++		
def fsm_evolution():
	#random number between 0 and 64
	bit = random.randint(0,63)
	i = random.randint(0,100)
	if i < fsm.mutrate:
		#print "MUTATING", i
		#print fsm.bintab
		#print "bintab val", fsm.bintab[col]
		
		if fsm.bintab[bit] == 0:
			fsm.bintab[bit] = 1
		elif fsm.bintab[bit] == 1:
			fsm.bintab[bit] = 0
 
		#print "new bintab val", fsm.bintab[col]
		#time.sleep(3)
	
	#xor that bit in bintab
	#rerun simulation
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++		

#++++++++++++++FSM SIMULATION ONE LIFE CYCLE ITERATION+++++++++++++++++++++++++++++++++
def fsm_sim():
	maze_init()	
	robot_init()
	#load x index of population
	
	action = 0
	for life in range(robot.health):
		print"-------------------------------------------------------------------"
		print "Iteration ", life
		robot_getsensors(robot.x,robot.y,robot.heading)
		print "Got Sensors" 
		print "Robot Sensors", robot.sens
		print "Crash Warning Flag ", robot.CWarn
		print "fitness ", robot.fitness 
		fsm.action = fsm.table[robot.dsens]
		fsm_action()
		format_heading()
		maze2 = copy.deepcopy(maze.maze)
		maze2[robot.x][robot.y] = robot.mhead #format heading
		pp.pprint(maze2)
		print "robot.dsens = ", robot.dsens
		print "selected action ", fsm.action
		print"-------------------------------------------------------------------"
		time.sleep(0)#+++++++wait++++++++

		#now perform mutation	
	#print "the original fsm table"
	#print fsm.table	
	#fsm_create_binstr()#turn the action table into a binary string for bit mutation
	#fsm_evolution()
	#fsm_bin2str()
	#print "the mutated fsm table"
	#print fsm.table
		#now turn bintab back into the action table format		
		



#+++++++++++++++++ALL FSM IN ONE FINAL CALL+++++++++++++++++++++++++++++++++++++++++++++
def finite_state_machine():
	#fsm_gen_actions() #Randomly Generate the list of possible actions
	
	#Generate the population	
	i = 0
	while i in range(population.size):
		fsm_gen_actions() #randomly generate some actions, but this is in denary
		fsm_create_binstr()
		population.pop.append(fsm.bintab)
		i = i + 1
	#------------------------------------------------
	#----------test each genome----------------------
	#choose the genome to test
	x = 0
	masit = 0
	while x in range(population.size):
		fsm.bintable = population.pop[x] #get genome in x index, load it into finite state machine class
		#convert the binary table to denary to run the sim, this is stupid but cont be bothered to change a load of code
		fsm_bin2str()
		fsm_sim()
		x = x + 1 # increment through the population
	print "DONE"	

	#litte bit to print out the entire population
	j = 0 
	while j in range(population.size):
		print population.pop[j]
		j = j + 1
	#--------------------------------------------
	#pp.pprint (population.pop)
	#print population.pop[2]
	
	#while robot.fitness < 19:
	#	fsm_sim()
	#	time.sleep(0)
	#	filewrite_fitness()
	#	filewrite_genome()

	#print "ROBOT FOUND THE FINISH"
	
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
pp.pprint(maze.maze)

print "The Numpy Maze"
print maze.nmaze


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



	
