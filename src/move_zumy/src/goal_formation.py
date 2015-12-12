#!/usr/bin/env python

#This function calculates the desired final state of the Zumys
#based on the user input command and the Zumy's current state

def decision(indicator, state):

	#Isolate the orientation and position of the Zumy in the current state dictionary
	x = state['x']
	y = state['y']
	theta = state['theta']

	#Set a buffer for orientation (in degrees)
	orientation_threshold = 45

	#Set a predefined amount to move linearly if the appropriate command is given (in units of the unit vector)
	lin_dist = .2

	#If the Zumys are in orientation theta = 0
	if  (abs(theta) <= orientation_threshold):

		#Assign goal state based on orientation
		if (indicator == 'left'):
			goal = {'x': x, 'y': y, 'theta': 90}
		elif (indicator == 'right'):
			goal = {'x': x, 'y': y, 'theta': -90}
		elif (indicator == 'forward'):
			goal = {'x': (x + lin_dist), 'y': y, 'theta': 0}
		elif (indicator == 'backward'):
			goal = {'x': (x - lin_dist), 'y': y, 'theta': 0} 

	#If the Zumys are in orientation theta = 90
	elif (theta < (90 + orientation_threshold)) and (theta > (90 - orientation_threshold)): 

		#Assign goal state based on orientation
		if (indicator == 'left'):
			goal = {'x': x, 'y': y, 'theta': 180}
		elif (indicator == 'right'):
			goal = {'x': x, 'y': y, 'theta': 0}
		elif (indicator == 'forward'):
			goal = {'x': x, 'y': (y + lin_dist), 'theta': 90}
		elif (indicator == 'backward'):
			goal = {'x': x, 'y': (y - lin_dist), 'theta': 90}

	#If the Zumys are in orientation theta = +/- 180
	elif (abs(theta) >= (180 - orientation_threshold)):

		#Assign goal state based on orientation
		if (indicator == 'left'):
			goal = {'x': x, 'y': y, 'theta': -90}
		elif (indicator == 'right'):
			goal = {'x': x, 'y': y, 'theta': 90}
		elif (indicator == 'forward'):
			goal = {'x': (x - lin_dist), 'y': y, 'theta': 180}
		elif (indicator == 'backward'):
			goal = {'x': (x + lin_dist), 'y': y, 'theta': 180}

	#If the Zumys are in orientation theta = -90
	elif (theta < (-90 + orientation_threshold)) and (theta > (-90 - orientation_threshold)): 

		#Assign goal state based on orientation
		if (indicator == 'left'):
			goal = {'x': x, 'y': y, 'theta': 0}
		elif (indicator == 'right'):
			goal = {'x': x, 'y': y, 'theta': -180}
		elif (indicator == 'forward'):
			goal = {'x': x, 'y': (y - lin_dist), 'theta': -90}
		elif (indicator == 'backward'):
			goal = {'x': x, 'y': (y + lin_dist), 'theta': -90}

	print theta
	return goal



