import math
sim_tim_scale = 0.05 	# should be seconds
turnInPlaceThresh = 30 	# if robot's heading is this many degrees or more from desired heading, just turn
maxFwdSpd  = .18			# max acceptable absolute value for linear.x
maxTurnSpd = .2			# max acceptable absolute value for angular.z	
distThresh	= 0.05		# when we are this close to the target point (in the new coordinate frame), then turn and fix orientation to goal['theta']
distThreshHigh = 0.15
finalHeadingThresh = 5  # when we are this many degrees away from the target orientation, stop moving.
finalTurnSpd = .15		# when we are really close in location and orientation, this is how slowly we turn		
#zumy_ar_pair = {'zumy5b': 'ar_marker_3', 'zumy5c': 'ar_marker_5', 'zumy7a': 'ar_marker_6'} #define Zumy-AR tag pairs

