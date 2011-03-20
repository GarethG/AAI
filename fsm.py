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
import pipes

numpy.set_printoptions(threshold=sys.maxint) #numpy likes to print large arrays wierd, supress this

#+++++++++++++++++++++File input args+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
fitness = open('./data/fitness.txt','a') #opens bestfit file, arg 'a' opens the file for appending data
genome = open('./data/genome.txt','a')

#++++++++++++++++WRITE TO FILE+++++++++++++++++++++++++++++++++++++++++++++++++++
def Filewrite_Fitness():
	fit = Robot.fitval
	fit = str(fit)	
	fitness.write (fit)
	fitness.write(' \n')	

def Filewrite_Genome(): #write the whole genome to a file
	for i in range(Population.size):
		gen = Population.genome[i]
		gen = str(gen)
		genome.write(gen)
		genome.write(' \n')

#+++++++++++++++WRITE TO THE PIPES!!+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Write into pipes in linux (not sure if this will work in windows), read this using another 
#python script, functionality such as rolling average fitness and plot will be cleaner this way

#--------------SETUP THE PIPES--------------------------------
#
t = pipes.Template()
t.append('tr a-z A-Z', '--')
f = t.open('/tmp/fsmfitness','w')
f.write('Initialised Pipe')
f.close()

t = pipes.Template()
t.append('tr a-z A-Z', '--')
f = t.open('/tmp/fsmgeneration','w')
f.write('Initialised Pipe')
f.close()


#-------------WRITE TO THE PIPES-----------------------------
#
def Pipe_Write_Fitness():
	f  = t.open('/tmp/fsmfitness','w')
	data = str(Robot.fitval)	
	f.write(data)
	f.close

def Pipe_Write_Generation():
	f  = t.open('/tmp/fsmgeneration','w')
	data = str(Population.generation)	
	f.write(data)
	f.close


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
	sens = [0,0,0,0,0] 	#[left, leftd, fwd, rightd, right]
	dsens = 0 		#Denary Sensor Values
	cwarn = 0 		#Crash Warning Flag
	genome = []

	

#++++++++++POPULATION CLASS+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Population:
	size = 50		#Size of Population
	genome = [] 		#all the genome's of the population
	genlen = 64		#length of the genome	
	fitness = [] 		#the fitness's of all the population
	mutrate = 30
	generation = 0
	tourn = []
	tournfit = []

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

#------------INIT POPULATION-----------------------------------------------------------------------------INIT POPULATION
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
	#print "entered del tile"
	if Maze.nmaze[Robot.x , Robot.y] == 1:
		#print "I should delete a tile"
		Maze.nmaze[Robot.x , Robot.y] = 0#[Robot.x][Robot.y] = 0 #if Robot has passed through a tile == 1 then make it 3 to show its path
		Maze.maze = Maze.nmaze.tolist()	#copy the numpy maze back into the standard maze, just for drawing	
		#time.sleep(1)
	#print "current maze position val in numpy ", Maze.nmaze[Robot.x , Robot.y]
	#print "current maze position val in list array ", Maze.maze[Robot.x][Robot.y]


#---------------ROBOT FITNESS FUNCTION-------------------------------------------------------------------ROBOT FITNESS FUNCTION
#
#If the Robot is on a tile then add 1 to its fitness
#
def Robot_Fitness():
	print "fitness call X, Y positions", Maze.nmaze[Robot.x , Robot.y]
	#print "robot fitness ", Robot.fitval
	if Maze.nmaze[Robot.x , Robot.y] == 1:#[Robot.x][Robot.y] == 1: #if the Robot is in a trail tile then add one to the fitness		
		Robot.fitval = Robot.fitval + 1
		print "fitness added"
	else:
		pass

#--------------BINARY TO DENARY CONVERTER------------------------------------------------------------------BINARY TO DENARY CONVERTER
#
#irritating hacky code to convert 2 binary bits into one denary value
#
def Bin_2_Den(binstr):
	denstr = [] #denary string 
	j = 0
	k = 0
	length = len(binstr)
	for k in range(0,length,2):
		j = k + 2
		if binstr[k:j] == [0,0]:
			denstr.append(0) # or 00

		elif binstr[k:j] == [0,1]:
			denstr.append(1) # or 01
			
		elif binstr[k:j] == [1,0]:
			denstr.append(2) # or 10
			
		elif binstr[k:j] == [1,1]:
			denstr.append(3) # or 11
			
		
	return denstr #return the denary string

#--------------GENERATE GENOME FUNCTION-------------------------------------------------------------------GENERATE GENOME FUNCTION
#
#Generate a binary bit pattern of a specified size
#
def Gen_Genome(size): 
	table = []
	for row in range(size): #size is passed in from the call
		table.append(random.randint(0,1))#append random value at the end of table
	return table #return a single bit pattern, size large

#---------------TOURNAMENT SELECTION---------------------------------------------------------------------TOURNAMENT SELECTION
#
#randomly pick 3 genomes
#take the fitest and put it in the tournament population
def Tournament_Sel():
	
	for i in range(Population.size):		
		#one tournament selection iteration
		can0 = random.randint(0,Population.size) #Candidate 1 index, can be used to access the fitness and the genome
		can1 = random.randint(0,Population.size) #Candidate 2 index
		can2 = random.randint(0,Population.size) #Candidate 3 index
		canlist = [can0, can1, can2]	

		canfit = [Population.fitness[can0] , Population.fitness[can1] , Population.fitness[can2]] #candidate fitness
		best = max(canfit) #highest fitness in canfit
		bestind = canfit.index(best) #index of the fitest
	
		Population.tournfit.append(Population.fitness[canlist[bestind]]) #lol take the index of the best candidate fitness, then use that to index the actual index from the original population index
		Population.tourn.append(Population.genome[canlist[bestind]]) #haha same ^^
	#now check the total fitness of the tournament candidate against the original population, if its lower then throw them out, if its higher, overwrite the current population with the tournament 
	oldfit = 0
	newfit = 0
	
	oldfit = sum(Population.fitness)
	newfit = sum(Population.tournfit)

	if oldfit > newfit:
		Population.tournfit = 0 #effectively do nothing, dont do anything to the actual population
		Population.tourn = 0

	if oldfit < newfit:
		Population.fitness = Population.tournfit #tournament selection succeeded, overwrite old genome with new
		Population.genome = Population.tourn	

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
			print"North Border in front"
			print"cwarn raised"
			#time.sleep(7)

		if Robot.sens[0] == 2: #if left is at border
			Robot.sens[0] = Maze.nmaze[x , PwrapY]
	
		if Robot.sens[4] == 2: #if right is at  border
			Robot.sens[4] = Maze.nmaze[x , MwrapY]
	
	#++++++++++++++++EAST WRAPPING+++++++++++++++++++++++++++++	
	elif Robot.heading == 1: #east

		if Robot.sens[2] == 2: #front
			Robot.sens[2] = Maze.nmaze[x , MwrapY]
			Robot.cwarn = 1
			print"east border in front"
			print"cwarn raised"
			#time.sleep(7)

		if Robot.sens[0] == 2: #left is at border
			Robot.sens[0] = Maze.nmaze[PwrapX , y]

		if Robot.sens[4] == 2: #if right is at border
			Robot.sens[4] = Maze.nmaze[MwrapX , y]

	#+++++++++++++++SOUTH WRAPPING+++++++++++++++++++++++++++
	elif Robot.heading == 2: #SOUTH
		
		if Robot.sens[2] == 2:
			Robot.sens[2] = Maze.nmaze[MwrapX , y]
			Robot.cwarn = 1
			print"south border in front"
			print"cwarn raised"
			#time.sleep(7)
		if Robot.sens[0] == 2:
			Robot.sens[0] = Maze.nmaze[x , MwrapY]

		if Robot.sens[4] == 2:
			Robot.sens[4] = Maze.nmaze[x , PwrapY]

	#+++++++++++++++WEST WRAPPING++++++++++++++++++++++++++
	elif Robot.heading == 3: #WEST

		if Robot.sens[2] == 2:
			Robot.sens[2] = Maze.nmaze[x , PwrapY]
			Robot.cwarn = 1
			print"west border in front"
			print"cwarn raised"
			#time.sleep(7)
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
	print "Got Sensors"

#-----------LOAD NEW GENOME----------------------------------------------------------------------LOAD NEW GENOME
#
#Load a new genome into the robot for simulation
#
def Robot_Load(num): 
	Robot.genome = Population.genome[num]
	print "loaded a genome into the robot"

#-----------ROBOT ACTION SELECTOR-----------------------------------------------------------------ROBOT ACTION SELECTOR
#
#Pick an action from the genome using the sensor data, drive the robot accordingly
#
def Robot_Action():
	#take in the denary sensor value, go to that index number in the genome, do that action
	#the genome is in binary, so first convert from 64 bit binary to 32 possible actions
	#i know i know, ineffcient...sue me
	acttab = []
	action = 0
	print "Robot Binary Sensor Valuse ",Robot.sens
	print "Robot Denary Sensor Value ",Robot.dsens
	acttab = Bin_2_Den(Robot.genome)
	action = acttab[Robot.dsens]
	
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
				print "wrapping robot at X Co-ord", Robot.x
				Robot.x = Robot.x + 7 #your at a border dont drive into that, so wrap to top of maze
				#time.sleep(5)				
				Robot.cwarn = 0 #reset crash flag
			elif Robot.cwarn == 0: #was just an else 
				Robot.x = Robot.x - 1						     

		elif Robot.heading == 1: #heading east								
			if Robot.cwarn == 1:
				print "wrapping robot at X Co-ord", Robot.x
				Robot.y = Robot.y - 7
				#time.sleep(5)
				Robot.cwarn = 0			
			elif Robot.cwarn == 0: #was just an else
				Robot.y = Robot.y + 1							
		
		elif Robot.heading == 2: #heading south
			if Robot.cwarn == 1:
				print "wrapping robot at X Co-ord", Robot.x
				Robot.x = Robot.x - 7
				#time.sleep(5)				
				Robot.cwarn = 0							
			elif Robot.cwarn == 0: #was just an else
				Robot.x = Robot.x + 1		
							
		elif Robot.heading == 3: #heading west
			if Robot.cwarn == 1:
				print "wrapping robot at X Co-ord", Robot.x
				#time.sleep(5)				
				Robot.cwarn = 0
				Robot.y = Robot.y + 7							
			elif Robot.cwarn == 0: #was just an else
				Robot.y = Robot.y - 1
		
		Robot_Fitness()	
		Robot.cwarn = 0
		Del_Tile()#delete the tile your on so you dont count its fitness more than once
	print "FSM - One Pass"
	print '\n'

#----------------MUTATION------------------------------------------------------------------------MUTATION
#
#Perform bitwise XOR on some bits to mutate the genome
#
def Genome_Mutation(gen):
	bit = random.randint(0,63)
	i = random.randint(0,100)
	if i < Population.mutrate:
		print "Mutating at bit ", bit
		if gen[bit] == 0:
			gen[bit] = 1
		elif gen[bit] == 1:
			gen[bit] = 0
	return gen

#-------------PRINT THE ENTIRE POPULATION-----------------------------------------------------PRINT THE ENTIRE POPULATION
#
#Just for debugging, print the population, nicely formatted
#
def Print_Genome():
	i = 0
	for i in range (Population.size):
		print "Genome Number", i, #"is ", len(Population.genome[i]), "bits long"	
		print Population.genome[i]
		i = i + 1
#---------------FINITE STATE MACHINE---------------------------------------------------------FINITE STATE MACHINE
#
#
#
def Finite_State_Machine():
	count = 0
	life = 0
	test = 0
	for test in range(Population.size):
		Robot_Load(test) #Load a new genome into the robot		
		iteration = 0 #count the number of times you've run through this loop

		for life in range(Robot.health):
			Get_Sensors()
			Robot_Action()
			Format_Heading()
			maze2 = copy.deepcopy(Maze.maze) #this is just for formating
			maze2[Robot.x][Robot.y] = Robot.format_head #format heading
			pp.pprint(maze2)
			print "Robot Fitness ", Robot.fitval
			print "The Iteration is ", iteration
			print "life var = ", life
			iteration = iteration + 1
			#print "cwarn = ", Robot.cwarn
			#time.sleep(0.3)

		Population.fitness.insert(Robot.fitval, test) #save this iterations fitness into the population class
		Pipe_Write_Fitness()
		Filewrite_Fitness() #save the fitness from this robot	
		print "Done an iteration"
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		#print "Starting a new pass with a new robot, same genome"		
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		print '\n'
		#time.sleep(2)
		
		#Del_Tile()
		#print "Old Genome ", Robot.genome
		Genome_Mutation(Robot.genome) #mutate the genome your using
		Init_Robot() #done an iteration so reset the robot
		Init_Maze() #done an iteration so reset the maze
		Population.generation =  Population.generation + 1
		Pipe_Write_Generation()
		
		
#----------------DEBUG FUNCTION -- DRIVE FORWARDS--------------------------------------------DEBUG FUNCTION -- DRIVE FORWARDS
#
#Test the wrapping code
#
def Debug_Drive():
	for i in range(250):
		Robot.heading = 2
		Get_Sensors()
		print Robot.sens
		#Robot.x = Robot.x - 1 
		if Robot.cwarn == 1: #crash warning raised
			print "wrapping robot", Robot.y
			Robot.x = Robot.x - 7 #your at a border dont drive into that, so wrap to top of maze
			Robot.cwarn = 0 #reset crash flag
		else:# Robot.cwarn == 0: 
				Robot.x = Robot.x + 1			

		Format_Heading()
		maze2 = copy.deepcopy(Maze.maze) #this is just for formating
		maze2[Robot.x][Robot.y] = Robot.format_head #format heading
		pp.pprint(maze2)
		time.sleep(1)
		Get_Sensors()
		print "Sensors", Robot.sens , "X Co-ord", Robot.x, "Y Co-ord", Robot.y
		print '\n'
	print "Done"

#-----------DEBUG FUNCTION -- LINE FOLLOWER-----------------------------------------------------DEBUG FUNCTION -- LINE FOLLOWER
#
#just a basic line folllower to test fitness and delete tile
#	
def Debug_Line_Follow():
	Format_Heading()
	maze2 = copy.deepcopy(Maze.maze) #this is just for formating
	maze2[Robot.x][Robot.y] = Robot.format_head #format heading
	pp.pprint(maze2)
	
	for i in range(25):	
		Get_Sensors()
		#+++++++++++++++FORWARD++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		if Robot.sens[2] == 1:								#	N	
			if Robot.heading == 0: #heading north					#	|
				Robot.x = Robot.x - 1						#    W--0--E 
			elif Robot.heading == 1: #heading east					#	|		
				Robot.y = Robot.y + 1						#	S
			elif Robot.heading == 2: #heading south					#		
				Robot.x = Robot.x + 1						#			
			elif Robot.heading == 3: #heading west							
				Robot.y = Robot.y - 1
		
		#++++++++++++++++TURN LEFT+++++++++++++++++++++++++++++++++++++++++++++++++++++++
		elif Robot.sens[0] == 1: #Turn Left
			if Robot.heading == 0: 		#Heading at North, make your heading West
				Robot.heading = 3
			elif Robot.heading == 1: 		#Heading at East, make your heading North
				Robot.heading = 0
			elif Robot.heading == 2: 		#Heading at South, make your heading East
				Robot.heading = 1
			elif Robot.heading == 3:		#Heading at West, make your heading South
				Robot.heading = 2
	
		#+++++++++++++++TURN RIGHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++
		elif Robot.sens[4] == 1:
			if Robot.heading == 0: 		#Heading at North, make your heading East
				Robot.heading = 1	
			elif Robot.heading == 1: 		#heading at East, make your heading South						
				Robot.heading = 2 			
			elif Robot.heading == 2: 		#heading at South, make your heading West
				Robot.heading = 3
			elif Robot.heading == 3: 		#heading at West, make your heading North
				Robot.heading = 0			
		
		Get_Sensors()
		Robot_Fitness() #eval the fitness of the robot
		Del_Tile() #remove the tile robot is currently in
		Format_Heading()
		maze2 = copy.deepcopy(Maze.maze) #this is just for formating
		maze2[Robot.x][Robot.y] = Robot.format_head #format heading
		pp.pprint(maze2)
		time.sleep(1)
		Get_Sensors()
		print "Sensors", Robot.sens , "X Co-ord", Robot.x, "Y Co-ord", Robot.y
		print "Fitness", Robot.fitval
		print '\n'

#++++++++++++++++MAIN++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++MAIN
Init_Maze()
Init_Robot()
Init_Population()	
#Print_Genome()

#Robot_Load(1)
Finite_State_Machine()
#Debug_Drive()
#Debug_Line_Follow()


	#print "New Genome ", Robot.genome
#pp.pprint (Maze.maze)
#print Maze.nmaze

