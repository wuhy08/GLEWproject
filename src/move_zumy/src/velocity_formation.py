#!/usr/bin/env python

import numpy
import rospy
import math

#This function calculates the angular and linear velocities that should be sent to the Zumys
#based on their current states and goal states

def getVel(state, goal):

	# PARAMETERS
	#######################################################################################

	#If the Zumys are instructed to turn left or right, they will do so until they are less than 
	#this amount off from the goal (in degrees)
	#NOTE: There is also a fine tuning theshold for final orientation checks
	TurnThreshold = 10
	TurnThreshold_fine = 2

	#The speed at which the Zumys turn
	TurnSpd = .16
	# TurnSpd = .21

	#The speed at which the Zumys turn when fine tuning
	TurnSpd_fine = .14

	#If the Zumys are instructed to drive forward or backward, they will do so until they are less than 
	#this amount off from the goal (in units of the unit vector created by our ground coordinate system)
	DriveThreshold = .11

	#The speed at which the Zumys drive
	DriveSpd = .10
	# DriveSpd = .15

	# CODE
	########################################################################################

	#Compute the angular difference between the goal state and the current state
	#NOTE: The only allowable values of del_heading  are between +/- 90 degrees.
	#      If del_heading is less than TurnThreshold, this infers that the Zumy 
	#	   was instructed to move forward or backward.
	#NOTE: If the Zumys are in a state where theta = 180, we need to do things differently because
	#      Haoyu's code casts theta to values of +/- 180.  We use the value 150 to include all values
	#      close to 180.  In particular we are concerned with the following two cases
	#			1. The current state is on the positive side of 180 and the goal state is theta = -90
	#			2. The current state is on the negative side of 180 and the goal state is theta = 90
	isReachGoal = False


	if (abs(state['theta']) > 150):

		#Adjust for case 1
		if ((numpy.sign(state['theta']) == 1) and (numpy.sign(goal['theta']) == -1)):
			del_heading = goal['theta'] + state['theta'] + 2*(180 - abs(state['theta']))

		#Adjust for case 2
		elif ((numpy.sign(state['theta']) == -1) and (numpy.sign(goal['theta']) == 1)):
			del_heading = goal['theta'] + state['theta'] - 2*(180 - abs(state['theta']))

		#If neither of these cases, just assign normally
		else:
			del_heading = goal['theta'] - state['theta']

	#Otherwise, we calculate del_heading normally
	else:
		del_heading = goal['theta'] - state['theta']

	print del_heading


	#Compute the linear difference between the goal state and current state in the x and y directions
	#NOTE: Only one of del_x and del_y should be greater than DriveThreshold at any given time.  
	#	   This value will be called delta. The only acceptable values of delta are between +/- del, 
	#      which is the fixed distance that a Zumy moves forward or backward when given a forward or 
	#	   backward command.  If delta is zero, this infers that the Zumy was instructed to turn left
	#	   or right.
	del_x = goal['x'] - state['x']
	del_y = goal['y'] - state['y']

	#If the Zumys are instructed to drive in the y direction
	if (abs(del_x) < DriveThreshold) and (abs(del_y) > DriveThreshold):
		delta = del_y

	#If the Zumys are instructed to drive in the x direction
	elif (abs(del_y) < DriveThreshold) and (abs(del_x) > DriveThreshold):
		delta = del_x

	#If both del_y and del_x are below the threshold, we assume that the Zumys should only be turning
	elif (abs(del_y) < DriveThreshold) and (abs(del_x) < DriveThreshold):
		delta = 0

	#If (due most likely to error) we get both del_x and del_y to be above DriveThreshold
	#we need to have a way to determine if either of them should have been above DriveThreshold
	#or if they both should have been below
	elif (abs(del_y) > DriveThreshold) and (abs(del_x) > DriveThreshold):

		#Find the larger of the two values (this is the one of question)
		tester = max(abs(del_x), abs(del_y))

		#If the larger of del_x and del_y is significantly over the DriveThreshold, we assume a
		#drive command was desired
		if (tester > (DriveThreshold + .5)):
			delta = tester

		#Otherwise, we assume that a turn was desired and sensor error produced the incorrect result
		else:
			delta = 0

	print delta

	#If a command to turn the Zumys left or right is given and the Zumys still have room to turn
	#This also can account for if the Zumys are commanded to drive but are initially very out of orientation
	if (abs(del_heading) > TurnThreshold):

		#The Zumys will not advance linearly
		lin_x = 0

		#If the command is to turn the Zumys to the left
		if (del_heading > TurnThreshold):

			#Rotate Zumys to the left
			ang_z = TurnSpd
			print("LEFT")

		#If the command is to turn the Zumys to the right
		elif (del_heading < -TurnThreshold):

			#Rotate Zumys to the right
			ang_z = -TurnSpd
			print("RIGHT")

	#If the Zumys need to move forward but are too far off their desired orientation
	#This also can account for if the Zumys were instructed to turn and are near their goal
	elif ((abs(del_heading) < TurnThreshold) and (abs(del_heading) > TurnThreshold_fine)):
	
		#Zumys do not move linearly
		lin_x = 0

		#Here, we do an orientation check
		if (del_heading > TurnThreshold_fine):
			
			#The Zumys turn for fine tuning orientation
			ang_z = TurnSpd_fine
			print("LEFT FINE")

		elif (del_heading < -TurnThreshold_fine):

			#The Zumys turn for fine tuning orientation
			ang_z = -TurnSpd_fine
			print("RIGHT FINE")

	#If a command to drive the Zumys forward or backward is given and the Zumys still have room to drive
	if ((abs(del_heading) < TurnThreshold) and (delta != 0)):

		#The Zumys will not turn
		ang_z = 0

		#If the orientation is at theta = 180 or theta = -90 we need to switch things
		if ((abs(state['theta']) > 150) or ((state['theta'] > -120) and (state['theta'] < -60))):

			#If the command is to drive the Zumys forward
			if (delta > DriveThreshold):

				#Drive Zumys forward
				lin_x = -DriveSpd
				print("BACKWARD")

			#If the command is to drive the Zumys backward
			elif (delta < -DriveThreshold):

				#Drive Zumys backward
				lin_x = DriveSpd
				print("FORWARD")

		#If the orientation is a positive angle or zero exactly
		else:

			#If the command is to drive the Zumys forward
			if (delta > DriveThreshold):

				#Drive Zumys forward
				lin_x = DriveSpd
				print("FORWARD")

			#If the command is to drive the Zumys backward
			elif (delta < -DriveThreshold):

				#Drive Zumys backward
				lin_x = -DriveSpd
				print("BACKWARD")
	
	#If the Zumys are already close enough to the goal and are close enough to the correct orientation
	if ((delta == 0) and (abs(del_heading) < TurnThreshold_fine)):
		
			#Zumys are done
			lin_x = 0
			ang_z = 0
			print("NOTHING")
			isReachGoal = True		

	return ({'lin_x': lin_x, 'ang_z': ang_z}, isReachGoal)



# from move_zumy.srv import MPCSolver


# def sanitize_degree(deg, goal_degree):
# 	# if abs(deg) < 5:
# 	# 	return 0

# 	# if abs(deg - 180) < 5:
# 	# 	return 180

# 	if deg > -190 and deg < -60 and goal_degree != -90 and goal_degree != 0:
# 		return 360 + deg

# 	if deg > 140 and goal_degree == -90:
# 		return deg - 360

# 	return deg


# def getVel(state, goal):
# 	deg = state['theta']
# 	goal_deg = goal['theta']
# 	goal_deg = 180 if goal_deg == -180 else goal_deg
# 	mpc_solver = rospy.ServiceProxy('mpc_solver', MPCSolver, persistent=True)
# 	print('Calling MPC SOLVER!!!')
# 	# resp = mpc_solver(state.x, state.y, state.theta*(pi/180), goal.x, goal.y, goal.theta)
# 	print('GOALLLLLL:')
# 	print(goal)
# 	resp = mpc_solver(state['x'], state['y'], sanitize_degree(deg, goal_deg)*(math.pi/180), goal['x'], goal['y'], goal_deg*(math.pi/180))
# 	dic = {'ang_z': resp.v_rt, 'lin_x': resp.v_tr}
# 	print('Velocities: ' + str(dic))
# 	return dic