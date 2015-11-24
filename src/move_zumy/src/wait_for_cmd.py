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
import config

#Creat class MoveZumy, all the publishing, subscribing and Service will happen here
class MoveZumy:
	def __init__(self, zumy_name):
		rospy.init_node('move_zumy'+zumy_name)
		self.name = zumy_name
		self.position = ZumyCoord().position
		self.ARTag = config.zumy_ar_pair[self.name]
		#Will subscribe to corresponding AR tag postion 
		#and once get new message, call getPos to update position
		rospy.Subscriber('/'+self.ARTag+'/AR_position', ZumyCoord, self.getPos)
		self.rate = rospy.Rate(10)
		self.goal = self.position
		self.goal_flag = True
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
		self.position = msg.position
		#print self.position

	def move(self, request):

		self.goal = request.goal
		#self.goal_flag = False
		#self.goalCounter = 0
		
		cmd = Twist()	
		cmd.linear.y = 0
		cmd.linear.z = 0
		cmd.angular.x = 0
		cmd.angular.y = 0

		#Creating a new current state based on the information from Haoyu's code		
		#Plugging the information from Haoyu's code into Vijay's getCmdVel function to calculate v_x and omega_z
		#while self.goalCounter<5:
		(vel, self.goal_flag) = get_vel.getCmdVel(self.position, self.goal)

	#Creating the ability to publish to the zumy

	#Creating the message type to publish to the zumy (information from vel)

		if (not self.goal_flag) and self.moveEnable:
			cmd.angular.z = vel['ang_z']
			cmd.linear.x = vel['lin_x']
			#self.goalCounter = 0
		if self.goal_flag and self.moveEnable:
			cmd.angular.z = 0
			cmd.linear.x = 0
			#self.goalCounter = self.goalCounter + 1
		if not self.moveEnable:
			cmd.angular.z = 0
			cmd.linear.x = 0
			#self.goalCounter = 0				

		#Publish new velocity information to the zumy
		self.vel_pub.publish(cmd)
		print cmd.linear.x
		print cmd.angular.z
		self.rate.sleep()

		return self.goal_flag
	
if __name__=='__main__':

	#Checks the number of arguments
	if len(sys.argv) < 2:
		print('Wrong Number of Arguments!  Use: move_to_location.py [ zumy name ]')
		sys.exit()
	little_zumy = MoveZumy(sys.argv[1])
	little_zumy.run()
