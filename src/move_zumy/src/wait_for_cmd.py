#!/usr/bin/env python
import rospy
import sys
import math
from ar_coord.msg import ZumyCoord
from geometry_msgs.msg import Twist,Transform,TransformStamped
from tf2_msgs.msg import TFMessage
from std_msgs.msg import Bool
from move_zumy.srv import Mov2LocSrv, Mov2LocSrvResponse
import get_vel
import get_vel_2 
import get_vel_3 as gv

import velocity_formation

from move_zumy.srv import AStarSolver
from geometry_msgs.msg import Pose2D

#Creat class MoveZumy, all the publishing, subscribing and Service will happen here
class MoveZumy:
	def __init__(self, zumy_name, ar_tag_num):
		rospy.init_node('move_zumy'+zumy_name)
		self.name = zumy_name
		self.position = ZumyCoord().position
		self.prevPosition = ZumyCoord().position
		self.posUnkown = True
		self.ARTag = 'ar_marker_'+ ar_tag_num
		#Will subscribe to corresponding AR tag postion 
		#and once get new message, call getPos to update position
		rospy.Subscriber('/'+self.ARTag+'/AR_position', ZumyCoord, self.getPos)
		self.rate = rospy.Rate(40)
		self.goal = self.position
		self.goal_flag = True
		self.historyNearGoal = False
		self.alpha = 0.9
		#self.goalCounter = 0
		#moveEnable will enable or disable the movement of Zumy
		self.moveEnable = True
		#The permission will be published by a topic that is responsible for coordinating zumys
		#TODO: may need another property that is responsible for channging zumy's route
		rospy.Subscriber('/'+self.name+'/MovePermission', Bool, self.updatePermission)
		# The publisher will be responsible for publishing zumy's velocity
		self.vel_pub = rospy.Publisher('/%s/cmd_vel' % self.name, Twist, queue_size=2)
		#The service will receive position request from clients
		rospy.Service('/'+self.name+'/zumy_tracking', Mov2LocSrv, self.move)
                self.astar = rospy.ServiceProxy('astar_solver', AStarSolver, persistent=True)
		print self.name+' is alive'

	#updatePermission will be called to update moveEnable whenever a new message is received from the topic
	def updatePermission(self, msg):
		self.moveEnable = msg.data

	# Just keep running the node
	def run(self):
		print self.name+ " is running"
		print self.goal
		rospy.spin()
	#getPos will be called to update zumy's position when receive a new message from topic
	def getPos(self, msg):
		if self.posUnkown:
			self.position = msg.position
			self.prevPosition = msg.position
			self.posUnkown = False
		else:
			self.prevPosition = self.position
			self.position.x = self.alpha * msg.position.x +\
			 					(1-self.alpha) * self.prevPosition.x
			self.position.y = self.alpha * msg.position.y +\
			 					(1-self.alpha) * self.prevPosition.y
			self.position.theta = self.alpha * msg.position.theta +\
			 					(1-self.alpha) * self.prevPosition.theta
		#print self.position
	# def move_main(self, request):
	# 	if request.Type == 'formation':
	# 		result = self.move(request)
	# 	if request.Type == 'unison':
	# 		result = self.move_unison(request)
	# 	return result

	# def move_unison(self, request):
	# 	self.goal = request.goal
	# 	#print self.name
	# 	#self.goal_flag = False
	# 	#self.goalCounter = 0
		
	# 	cmd = Twist()	
	# 	cmd.linear.y = 0
	# 	cmd.linear.z = 0
	# 	cmd.angular.x = 0
	# 	cmd.angular.y = 0

	


	def move(self, request):

		self.goal = request.goal
		#print self.name
		#self.goal_flag = False
		#self.goalCounter = 0
		
		cmd = Twist()	
		cmd.linear.y = 0
		cmd.linear.z = 0
		cmd.angular.x = 0
		cmd.angular.y = 0

                obstacle1 = Pose2D(30.0, 2.0, 0.0)

		#Creating a new current state based on the information from Haoyu's code		
		#Plugging the information from Haoyu's code into Vijay's getCmdVel function to calculate v_x and omega_z
		#while self.goalCounter<5:
		if request.Type == 'formation':
                        # start_point = 
                        # goal_point = Pose2D(self.goal.x, self.goal.y, self.goal.theta)
                        
                        intermediate_goal = self.astar([obstacle1], self.position, self.goal)

			(vel, self.goal_flag, self.historyNearGoal) = \
				# gv.getCmdVel(self.position, self.goal, self.name, self.historyNearGoal)
				gv.getCmdVel(self.position, intermediate_goal, self.name, self.historyNearGoal)


                        
		if request.Type == 'unison':
			position_unison = {'x':self.position.x,
								'y':self.position.y,
								'theta':self.position.theta}
			goal_unison = {'x':self.goal.x,
							'y':self.goal.y,
							'theta':self.goal.theta}
			(vel, self.goal_flag) = \
				velocity_formation.getVel(position_unison, goal_unison)
			self.historyNearGoal = True


	#Creating the ability to publish to the zumy

	#Creating the message type to publish to the zumy (information from vel)

		if (not self.goal_flag) and self.moveEnable:
			cmd.angular.z = vel['ang_z']
			cmd.linear.x = vel['lin_x']
			#self.goalCounter = 0
		if self.goal_flag:
			cmd.angular.z = 0
			cmd.linear.x = 0
			self.historyNearGoal = False
			#self.goalCounter = self.goalCounter + 1
		if not self.moveEnable:
			cmd.angular.z = 0
			cmd.linear.x = 0
			#self.goalCounter = 0				

		#Publish new velocity information to the zumy
		self.vel_pub.publish(cmd)
		print self.historyNearGoal
		#print cmd.linear.x
		#print cmd.angular.z
		self.rate.sleep()

		return self.goal_flag
	
if __name__=='__main__':

	#Checks the number of arguments
	if len(sys.argv) < 3:
		print('Wrong Number of Arguments!  Use: move_to_location.py [ zumy name ] [ar tag number]')
		sys.exit()
	little_zumy = MoveZumy(sys.argv[1], sys.argv[2])
	little_zumy.run()
