#!/usr/bin/env python
import rospy
import sys
import math
from ar_coord.msg import ZumyCoord
from geometry_msgs.msg import Twist
import get_vel
import numpy
from numpy import linalg
import time

#rate = rospy.Rate(10)	


#Initializes a current state for both Zumys
current_state1 = {'x': 10, 'y': 0, 'theta': 0}
current_state2 = {'x': 0, 'y': 0, 'theta': 0}


def collide (state1, state2, min_safe_dist):
	#Computes the vector (x-y only) between the two Zumys
	zumy_vect = numpy.array([state2['x'] - state1['x'], state2['y'] - state1['y']])

	#Computes the Euclidean distance between teh two Zumys
	zumy_dist = linalg.norm(zumy_vect)

	#Determine if the Zumys are too close
	if zumy_dist < min_safe_dist:
		return True
	else:
		return False

def move(msg, arg):
	
	#Set rospy rate
	rate = rospy.Rate(10)

	#Expose variables from subscriber line
	zumy1 = arg[0]
	zumy1_tag = str('ar_marker_') + str(arg[1])
	goal1 = arg[2]

	zumy2 = arg[3]
	zumy2_tag = str('ar_marker_') + str(arg[4])
	goal2 = arg[5]
	
	#Allow the current state dictionaries to be treated as global variables within the callback function
	global current_state1
	global current_state2

	#Always update the current states of the Zumys
	if msg.zumyID == zumy1_tag:
		#Creating a new current state based on the information from Haoyu's code
		current_state1 = {'x': msg.position.x, 'y': msg.position.y, 'theta': msg.position.theta}
	
	elif msg.zumyID == zumy2_tag:
		#Creating a new current state based on the information from Haoyu's code
		current_state2 = {'x': msg.position.x, 'y': msg.position.y, 'theta': msg.position.theta}

	#Create the ability to publish to the Zumys
	zumy_vel1 = rospy.Publisher('/%s/cmd_vel' % zumy1, Twist, queue_size=2)
	zumy_vel2 = rospy.Publisher('/%s/cmd_vel' % zumy2, Twist, queue_size=2)

	#Creating the message type to publish to the Zumys and defining constant parameters
	cmd1 = Twist()
	cmd1.linear.y = 0
	cmd1.linear.z = 0
	cmd1.angular.x = 0
	cmd1.angular.y = 0
	
	cmd2 = Twist()
	cmd2.linear.y = 0
	cmd2.linear.z = 0
	cmd2.angular.x = 0
	cmd2.angular.y = 0

	#Determine what to do based on whether or not the Zumys will collide
	if not collide(current_state1, current_state2, .5):

		#Determine what state information is currently being sent across Haoyu's topic
		if msg.zumyID == zumy1_tag:
			print 'ZUMY1'

			#Plugging the information from Haoyu's code into Vijay's getCmdVel function to calculate v_x and omega_z
			vel1 = get_vel.getCmdVel(current_state1, goal1)
			
			#Update the message type to publish to zumy1
			cmd1.linear.x = vel1['lin_x']
			cmd1.angular.z = vel1['ang_z']

			#Publish new velocity information to zumy2
			zumy_vel1.publish(cmd1)
			rate.sleep()

		elif msg.zumyID == zumy2_tag:
			print 'ZUMY2'

			#Plugging the information from Haoyu's code into Vijay's getCmdVel function to calculate v_x and omega_z
			vel2 = get_vel.getCmdVel(current_state2, goal2)
			
			#Creating the message type to publish to zumy2
			cmd2.linear.x = vel2['lin_x']
			cmd2.angular.z = vel2['ang_z']

			#Publish new velocity information to zumy2
			zumy_vel2.publish(cmd2)
			# rate.sleep()
	
	elif collide(current_state1, current_state2, .5):
		print 'TOO CLOSE!'

		#Define the time when a collision was first detected
		collision_detection_time = time.time()

		#Initialize a current time
		current_time = time.time()

		while current_time - collision_detection_time < 2: 
			#Redefine the current time variable
			current_time = time.time()	

			#Hold Zumy1 temorarily
			cmd1.linear.x = 0
			cmd1.angular.z = 0

			#Back Zumy2 off
			cmd2.linear.x = -.15
			cmd2.angular.z = 0
			
			#Publish collision-avoidance twists to Zumys if they get too close
			zumy_vel1.publish(cmd1)
			zumy_vel2.publish(cmd2)
			rate.sleep()
			print 'IN LOOP!'
	
	# rate.sleep()

if __name__=='__main__':

	#Checks the number of arguments
	if len(sys.argv) < 5:
		print('Wrong Number of Arguments!  Use: move_to_location.py [ zumy1 name ], [ zumy1 tag number ], [ zumy2 name ], [ zumy2 tag number ]')
		sys.exit()

	#Initiates our node
	rospy.init_node('MoveZumy')
	
	#Defines parameters that ultimately get fed to our move function
	zumy1 = sys.argv[1]
	zumy1_tag = sys.argv[2]
	goal_state1 = {'x': .1, 'y': .1, 'theta': 0}
	# goal_state1 = {'x': 1, 'y': 1, 'theta': 180}

	zumy2 = sys.argv[3]
	zumy2_tag = sys.argv[4]
	goal_state2 = {'x': 1, 'y': 1, 'theta': 180}
	# goal_state2 = {'x': .1, 'y': .1, 'theta': 0}

	#Subscribes to the zumy_position topic created by Haoyu's code
	rospy.Subscriber('zumy_position', ZumyCoord, move, [zumy1, zumy1_tag, goal_state1, zumy2, zumy2_tag, goal_state2])
	rospy.spin()