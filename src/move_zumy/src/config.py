# Old stuff
sim_tim_scale = 0.05 	# should be seconds

# Goal checking thresholds
distThresh	= 0.05		# when we are this close to the target point (in the new coordinate frame), then turn and fix orientation to goal
distThreshHigh = 0.15	# variable for hysteresis (once distThresh has been met, just check if we are within distThreshHigh thereafter)
finalHeadingThresh = 5  # when we are this many degrees away from the target orientation, stop moving.

# Turning Parameters
turnInPlaceThresh = 15 	# if robot's heading is this many degrees or more from desired heading, just turn
slowTurnSpd = 0.4		# max turn speed when close to goal (within lookAheadPtDist)
maxTurnSpd = 0.4		# max turn speed when not near goal 
ang_z_ramp_up_spd = 0.1 # max |dw/dt| change allowed
finalTurnSpd = .1		# when we are really close in location and orientation, this is how slowly we turn		

# Forward Speed Parameters and LookAhead Dist
slowFwdSpd = 0.08			# max fwd speed when near the goal (within lookAheadPtDist)
maxFwdSpd  = .12			# max fwd speed when not near the goal
lin_x_ramp_up_spd = 0.1		# max |dv/dt| change allowed
lookAheadPtDist = 0.1		# if more than this distance away from the goal








