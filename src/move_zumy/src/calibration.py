#!/usr/bin/env python
import rospy
import sys
import math
from ar_coord.msg import ZumyCoord
from geometry_msgs.msg import Twist, Pose2D
from move_zumy.srv import Mov2LocSrv, Mov2LocSrvResponse
from std_msgs.msg import Bool, Time
#import get_vel
import config
import numpy as np
import assign_dest as ad
import collision_checker as cc
import collision_checker_tests as cct
import matplotlib.pyplot as plt


def confine_angle(old_angle):
	while old_angle>180 or old_angle<-180:
		if old_angle>180:
			old_angle = old_angle - 360
		elif old_angle<-180:
			old_angle = old_angle + 360
	return old_angle

class ZumyPosMonitor:
	def __init__(self, zumy_name, ar_tag_num):
		rospy.init_node('calibrate_zumy'+zumy_name)
		self.name = zumy_name
		self.position = ZumyCoord().position
		self.prevPos = ZumyCoord().position
		self.ARTag = 'ar_marker_'+ar_tag_num	
		rospy.Subscriber('/'+self.ARTag+'/AR_position', ZumyCoord, self.getPos)
		self.time = Time()
		self.prevTime = Time()
		self.rotSpd = 0
		self.rotSpdAcc = 0
		self.posUnkown = True
		self.alpha = 1
		self.vel_pub = rospy.Publisher('/%s/cmd_vel' % self.name, Twist, queue_size=2)
		self.data_num = 0
	def getPos(self, msg):
		if self.posUnkown:
			self.position = msg.position
			self.prevPosition = msg.position
			self.time = msg.time
			self.prevTime = msg.time
			self.posUnkown = False
		else:
			self.prevPosition = self.position
			self.prevTime = self.time
			self.time = msg.time
			self.position.x = self.alpha * msg.position.x +\
			 					(1-self.alpha) * self.prevPosition.x
			self.position.y = self.alpha * msg.position.y +\
			 					(1-self.alpha) * self.prevPosition.y
			self.position.theta = self.alpha * msg.position.theta +\
			 					(1-self.alpha) * self.prevPosition.theta
			self.getRotSpd()
	def getRotSpd(self):
		self.rotSpdAcc = confine_angle(self.position.theta - self.prevPosition.theta)/\
						(self.time - self.prevTime) + self.rotSpdAcc
		self.data_num = self.data_num + 1
	def average(self):
		self.rotSpd = self.rotSpdAcc/self.data_num
	def clear(self):
		self.rotSpdAcc = 0
		self.data_num = 0



if __name__== '__main__':
	rospy.init_node('calib_process')
	is_in_form = False
	is_goal_reached = True
	myargv = rospy.myargv()
	infl_radius = 0.06
	calib_times = 30
	rot_vel_dict = {}
	rate = rospy.Rate(10)
	if not len(myargv) in [3,5,7,9]:
		print('Wrong Number of Arguments!  We need to have valid Zumy and AR tag pairs')
		sys.exit()
	zumy_numbers = (len(myargv)-1)/2
	zumy_ID = myargv[1:zumy_numbers+1]
	ar_tag_nums = myargv[zumy_numbers+1:]
	for curr_zumy_ID in zumy_ID:
		zumy_monitor[curr_zumy_ID] = ZumyPosMonitor(curr_zumy_ID, ar_tag_nums[i])
		rot_vel_dict[curr_zumy_ID] = []
	twist_to_be_pub = Twist()
	twist_to_be_pub.linear.x = 0
	twist_to_be_pub.linear.y = 0
	twist_to_be_pub.linear.z = 0
	twist_to_be_pub.angular.x = 0
	twist_to_be_pub.angular.y = 0
	rot_vel_list = range(0, 0.25, 0.01)
	for curr_rot_vel in rot_vel_list:
		twist_to_be_pub.angular.z = curr_rot_vel
		for curr_zumy_ID in zumy_ID:
			zumy_monitor[curr_zumy_ID].clear()
			for ii in range calib_times:
				zumy_monitor[curr_zumy_ID].vel_pub.publish(twist_to_be_pub)
				rate.sleep()
			rot_vel_dict[curr_zumy_ID].append(self.rotSpd)
	print rot_vel_dict		


