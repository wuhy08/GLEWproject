#!/usr/bin/env python
import rospy
import sys
import math
from ar_coord.msg import ZumyCoord
from geometry_msgs.msg import Twist, Pose2D
from move_zumy.srv import Mov2LocSrv, Mov2LocSrvResponse
#import get_vel
import config
import numpy as np
import assign_dest as ad

class ZumyPosMonitor:
	def __init__(self, zumy_name):
		self.name = zumy_name
		self.position = ZumyCoord().position
		self.ARTag = config.zumy_ar_pair[self.name]		
		rospy.Subscriber('/'+self.ARTag+'/AR_position', ZumyCoord, self.getPos)
	def getPos(self, msg):
		self.position = msg.position

def send_loc_req_stat(zumy_name, goal_position):
	service_name = '/'+zumy_name+'/zumy_tracking'
	rospy.wait_for_service(service_name)
	try:
		send_goal_pos = rospy.ServiceProxy(service_name, Mov2LocSrv)
		goal_reach_flag = send_goal_pos(zumy_name, goal_position)
		return goal_reach_flag.isPosReached
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


def translate_cmd_2_coord(formation_string):
	if formation_string == 'h':
		coord = np.array([[0.1, 0.5, 90],
				[0.37, 0.5, 90],
				[0.63, 0.5, 90],
				[0.9, 0.5, 90]])
	if formation_string == 's':
		coord = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90],
				[0.8, 0.8, 90],
				[0.2, 0.8, 90]])
	if formation_string == 't':
		coord = np.array([[0.76, 0.35, 90],
				[0.24, 0.35, 90],
				[0.5, 0.8, 90],
				[0.5, 0.5, 90]])
	if formation_string == 'd':
		coord = np.array([[0.7, 0.5, 90],
				[0.5, 0.2, 90],
				[0.3, 0.5, 90],
				[0.5, 0.8, 90]])
	if formation_string == 'v':
		coord = np.array([[0.5, 0.2, 90],
				[0.5, 0.5, 90],
				[0.5, 0.8, 90],
				[0.5, 0.8, 90]])
	return coord

if __name__== '__main__':
	is_goal_reached = True
	myargv = rospy.myargv()
	if not len(sys.argv) == 5:
		print('Wrong Number of Arguments!  We need to have 4 Zumys')
		sys.exit()
	zumy_ID = myargv[1:]
	zumy_monitor = {}
	goal_pos_for_srv = {}
	for curr_zumy_ID in zumy_ID:
		zumy_monitor[curr_zumy_ID] = ZumyPosMonitor(curr_zumy_ID)

	predef_formation_command = ['h', 's', 't', 'd', 'v']
	while True:
		final_dest_counter = 0
		formation_command = raw_input("Please input formation command:")
		if formation_command in predef_formation_command:
			final_destination = translate_cmd_2_coord(formation_command)
			latest_zumy_pos = np.zeros((4,3))
			ii = 0
			for curr_zumy_ID in zumy_ID:
				latest_zumy_pos[ii] = np.array([zumy_monitor[curr_zumy_ID].position.x,
												zumy_monitor[curr_zumy_ID].position.y,
												zumy_monitor[curr_zumy_ID].position.theta])
				ii = ii + 1
			#Uncomment the following line to enable optimal path calculation 
			new_final_destination = ad.find_optimal_path(latest_zumy_pos, final_destination)
			#Uncomment the following line to disable optimal path calculation
			#new_final_destination = final_destination[0:3]
			ii = 0
			for curr_zumy_ID in zumy_ID:
				goal_pos_for_srv[curr_zumy_ID] = Pose2D()
				goal_pos_for_srv[curr_zumy_ID].x = new_final_destination[ii,0]
				goal_pos_for_srv[curr_zumy_ID].y = new_final_destination[ii,1]
				goal_pos_for_srv[curr_zumy_ID].theta = new_final_destination[ii,2]
				ii = ii + 1
			while final_dest_counter<5:
				zumy_reach_num = 0
				for curr_zumy_ID in zumy_ID:
					is_goal_reached = send_loc_req_stat(curr_zumy_ID, goal_pos_for_srv[curr_zumy_ID])
					if is_goal_reached:
						zumy_reach_num = zumy_reach_num + 1
				print zumy_reach_num
				if zumy_reach_num == 3:
					final_dest_counter = final_dest_counter + 1
				if not zumy_reach_num == 3:
					final_dest_counter = 0




		if not formation_command in predef_formation_command:
			print("Error! Please only input predefined command.")



		# goal_pos = Pose2D()
		# goal_pos.x = input("Please input "+zumy_ID+"\'s x coord:")
		# goal_pos.y = input("Please input "+zumy_ID+"\'s y coord:")
		# goal_pos.theta = input("Please input "+zumy_ID+"\'s theta coord in deg:")
		# is_goal_reached = send_loc_req_stat(zumy_ID, goal_pos)

