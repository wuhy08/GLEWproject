import math
import config
import matplotlib.pyplot as plt
import time
from geometry_msgs.msg import Pose2D

DEBUG = True
def print_debug(s):
	if DEBUG:
		print s

def e_dist(del_x, del_y):
	return math.sqrt(del_x*del_x + del_y*del_y)

def getMin(x1, x2):
	if(x1>x2):
		return x2
	return x1

def goToIntermediatePoint(state, goal, lookAheadPtDist, name):
	if lookAheadPtDist < e_dist(state.x-goal.x, state.y-goal.y):
		# Far from goal.  Just look at a target lookAheadPtDist away along the path vector - not the goal point itself.
		del_x_world = lookAheadPtDist*(goal.x - state.x)/e_dist(state.x-goal.x, state.y-goal.y)
		del_y_world	= lookAheadPtDist*(goal.y - state.y)/e_dist(state.x-goal.x, state.y-goal.y)
	else:
		# Adequately close to the goal, so we use the goal as the target point.
		del_x_world = goal.x - state.x
		del_y_world = goal.y - state.y

	desired_heading = math.atan2(del_y_world, del_x_world)
	desired_heading = math.degrees(desired_heading)

	# Compute difference in desired and current heading.  Cast to [-PI,PI].
	del_heading = desired_heading - state.theta
	if del_heading > 180:
		del_heading = del_heading - 360
	elif del_heading < -180:
		del_heading = del_heading + 360
	print_debug('%s: del_heading = %f' % (name, del_heading))
	print_debug('%s: desired_heading = %f' % (name, desired_heading))
        
        # time.sleep(1000000000)

	# Motor commands issued here.  Check if we need to turn first.
	if abs(del_heading) > config.turnInPlaceThresh:
		if del_heading > 0:
			lin_x = 0
			ang_z = config.maxTurnSpd
			print_debug('%s: Turning + to reach intermediate point' % name)
		else:
			lin_x = 0
			ang_z = -config.maxTurnSpd
			print_debug('%s: Turning - to reach intermediate point' % name)
	else:
		# Drive and turn at the same time.  Linear velocity scales with the amount of the distance along the robot's x-axis.
		# Angular velocity scales with the amount of the distance along the robot's y-axis (that we can't cover without turning).
		theta_rad = math.radians(state.theta)
		
		# Convert global world to local robot coordinates.
		del_x_robot = del_x_world * math.cos(theta_rad) + del_y_world * math.sin(theta_rad)
		del_y_robot = -del_x_world * math.sin(theta_rad) + del_y_world * math.cos(theta_rad)
	
		# Motor commands
		lin_x = config.maxFwdSpd * del_x_robot/e_dist(del_x_robot, del_y_robot)
		ang_z = config.maxTurnSpd * del_y_robot/e_dist(del_x_robot, del_y_robot)
	
	# Final check if motor commands are within bounds.
	if abs(lin_x) > config.maxFwdSpd:
		if lin_x > 0:
			lin_x = config.maxFwdSpd
		else:
			lin_x = -config.maxFwdSpd

	if abs(ang_z) > config.maxTurnSpd:
		if ang_z > 0:
			ang_z = config.maxTurnSpd
		else:
			ang_z = -config.maxTurnSpd

	return {'lin_x': lin_x, 'ang_z': ang_z}

def fixFinalHeading(state, goal, name):
	# Compute difference in desired and current heading.  Cast to [-PI,PI].
	del_heading = goal.theta - state.theta
	if del_heading > 180:
		del_heading = del_heading - 360
	elif del_heading < -180:
		del_heading = del_heading + 360
	print_debug('%s: del_heading = %f' % (name, del_heading))
	is_goal_reached = False

	if abs(del_heading) < config.finalHeadingThresh:
		ang_z = 0
		print_debug('%s: Reached goal' % name)
		is_goal_reached = True
	elif del_heading > 25:
		ang_z =  config.finalTurnSpd + (config.maxTurnSpd - config.finalTurnSpd)/155*(del_heading - 25)
		print_debug('%s: At goal, angle very +' % name)
	elif del_heading < -25:
		ang_z = -config.finalTurnSpd - (config.maxTurnSpd - config.finalTurnSpd)/155*(abs(del_heading) - 25)
		print_debug('%s: At goal, angle very -' % name)
	elif del_heading > 0:
		ang_z = config.finalTurnSpd
		print_debug('%s: At goal, angle small + but slowly converging' % name)
	elif del_heading < 0:
		ang_z = -config.finalTurnSpd
		print_debug('%s: At goal, angle small - but slowly converging' % name)

	# Final check if motor commands are within bounds.
	if abs(ang_z) > config.maxTurnSpd:
		if ang_z > 0:
			ang_z = config.maxTurnSpd
		else:
			ang_z = -config.maxTurnSpd
	lin_x = 0;
	return ({'lin_x': lin_x, 'ang_z': ang_z}, is_goal_reached)


def getCmdVel(state, goal, name, isPreviousNearGoal):
	# isPreviousNearGoal is an input from Haoyu's code.  It is assigned based on the return value of nearGoalPt below.
	# and lets us know if the Zumy had previously gotten close to the goal (so we are in an orientation fixing state).
	# is_goal_reached is an output flag that lets the client know that the Zumy has reached the goal.
	del_x_world = goal.x - state.x
	del_y_world = goal.y - state.y

	# Go to intermediate point if we are far from the goal and haven't yet previously reached the goal.
	# Addition of (not isPreviousNearGoal) is to prevent instability by forcing the Zumy to only fix orientation
	# once it has gotten close to the goal for the first time.

        cmd_vel = goToIntermediatePoint(state,goal, config.lookAheadPtDist, name)
        is_goal_reached = False # We have not reached the goal yet.
        nearGoalPt = False # Let the client know we haven't yet gotten close to the goal.


	# if(e_dist(del_x_world, del_y_world) > config.distThresh and (not isPreviousNearGoal)):
	# 	cmd_vel = goToIntermediatePoint(state,goal, config.lookAheadPtDist, name)
	# 	is_goal_reached = False # We have not reached the goal yet.
	# 	nearGoalPt = False # Let the client know we haven't yet gotten close to the goal.
	# else:
	# 	nearGoalPt = True # Let the client know that we have gotten close to the goal.  This output is
	# 					  # used to inform the client we are in an orientation fixing state.	
	# 	# Either output a twist command or let the client know we reached the goal
	# 	(cmd_vel, is_goal_reached) = fixFinalHeading(state,goal,name) 

	return (cmd_vel, is_goal_reached, nearGoalPt)

