#!/usr/bin/env python
import rospy
import sys
import math
from ar_coord.msg import ZumyCoord
from geometry_msgs.msg import Twist, Pose2D
from move_zumy.srv import Mov2LocSrv, Mov2LocSrvResponse
from std_msgs.msg import Bool
#import get_vel
import config
import numpy as np
import assign_dest as ad
import collision_checker as cc
import collision_checker_tests as cct
import matplotlib.pyplot as plt

class ZumyPosMonitor:
	def __init__(self, zumy_name, ar_tag_num):
		self.name = zumy_name
		self.position = ZumyCoord().position
		self.ARTag = 'ar_marker_'+ar_tag_num	
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


def translate_cmd_2_coord(formation_string, n):
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
		coord = np.array([[0.5, 0.1, 90],
				[0.5, 0.37, 90],
				[0.5, 0.63, 90],
				[0.5, 0.9, 90]]) # Edited by Vijay on 12-6 from [0.5, 0.8, 90] to [0.5, 1.1, 90]
	return coord[0:n]

if __name__== '__main__':
	DEBUG_PLOT = False
	if DEBUG_PLOT:
		plt.ion()
		plt.show()
	rospy.init_node('send_form')
	is_in_form = False
	is_goal_reached = True
	myargv = rospy.myargv()
	infl_radius = 0.05


	if not len(myargv) in [3,5,7,9]:
		print('Wrong Number of Arguments!  We need to have valid Zumy and AR tag pairs')
		sys.exit()
	zumy_numbers = (len(myargv)-1)/2
	zumy_ID = myargv[1:zumy_numbers+1]
	ar_tag_nums = myargv[zumy_numbers+1:]
	zumy_monitor = {}
	goal_pos_for_srv = {}
	latest_zumy_pos_cc = {}
	goal_pos_for_cc = {}
	zumy_vector_cc = {}
	zumy_move_premission = {}
	i=0
	move_permission_pub = {}
	for curr_zumy_ID in zumy_ID:
		zumy_monitor[curr_zumy_ID] = ZumyPosMonitor(curr_zumy_ID, ar_tag_nums[i])
		move_permission_pub[curr_zumy_ID]=rospy.Publisher('/'+curr_zumy_ID+'/MovePermission',
												Bool, queue_size = 2)
		i = i + 1

	predef_formation_command = ['h', 's', 't', 'd', 'v']
	predef_unison_command = ['f', 'b', 'l', 'r']
	while True:
		final_dest_counter = 0
		formation_command = raw_input("Please input formation command:")
		if (formation_command in predef_formation_command):
			final_destination = translate_cmd_2_coord(formation_command, zumy_numbers)
			latest_zumy_pos = np.zeros((zumy_numbers,3))
			ii = 0
			for curr_zumy_ID in zumy_ID:
				latest_zumy_pos[ii] = np.array([zumy_monitor[curr_zumy_ID].position.x,
												zumy_monitor[curr_zumy_ID].position.y,
												zumy_monitor[curr_zumy_ID].position.theta])
				ii = ii + 1
			#Uncomment the following line to enable optimal path calculation 
			new_final_destination = ad.find_optimal_path_n(latest_zumy_pos, final_destination)
			#Uncomment the following line to disable optimal path calculation
			#new_final_destination = final_destination[0:3]
			ii = 0
			for curr_zumy_ID in zumy_ID:
				goal_pos_for_srv[curr_zumy_ID] = Pose2D()
				goal_pos_for_srv[curr_zumy_ID].x = new_final_destination[ii,0]
				goal_pos_for_srv[curr_zumy_ID].y = new_final_destination[ii,1]
				goal_pos_for_srv[curr_zumy_ID].theta = new_final_destination[ii,2]
				ii = ii + 1
			while final_dest_counter<1:
				zumy_reach_num = 0
				for curr_zumy_ID in zumy_ID:
					latest_zumy_pos_cc[curr_zumy_ID] = cc.Point2D(zumy_monitor[curr_zumy_ID].position.x,
													zumy_monitor[curr_zumy_ID].position.y)
					goal_pos_for_cc[curr_zumy_ID] = cc.Point2D(goal_pos_for_srv[curr_zumy_ID].x,
														goal_pos_for_srv[curr_zumy_ID].y)
					zumy_vector_cc[curr_zumy_ID] = cc.Vector2D(latest_zumy_pos_cc[curr_zumy_ID], 
																goal_pos_for_cc[curr_zumy_ID])
				permission_result = cc.command_n_zumys(zumy_vector_cc, zumy_ID, infl_radius)
				for curr_zumy_ID in zumy_ID:
					zumy_move_premission[curr_zumy_ID] = permission_result[1][curr_zumy_ID]
				# cct.plot_bounding_boxes(permission_result[0].values(), 
				# 	cc.Vector2D(latest_zumy_pos_cc[zumy_ID[0]], goal_pos_for_cc[zumy_ID[0]]), 
				# 	cc.Vector2D(latest_zumy_pos_cc[zumy_ID[1]], goal_pos_for_cc[zumy_ID[1]]),  
				# 	cc.Vector2D(latest_zumy_pos_cc[zumy_ID[2]], goal_pos_for_cc[zumy_ID[2]]), 
				# 	cc.Vector2D(latest_zumy_pos_cc[zumy_ID[3]], goal_pos_for_cc[zumy_ID[3]]), 
				# 	infl_radius)
				# cct.plot_bounding_boxes(permission_result[0].values(), 
				# 	zumy_vector_cc.values(),
				# 	infl_radius)
				for curr_zumy_ID in zumy_ID:
					move_permission_pub[curr_zumy_ID].publish(zumy_move_premission[curr_zumy_ID])
					is_goal_reached = send_loc_req_stat(curr_zumy_ID, goal_pos_for_srv[curr_zumy_ID])
					if is_goal_reached:
						zumy_reach_num = zumy_reach_num + 1
				print zumy_reach_num
				if zumy_reach_num == zumy_numbers:
					final_dest_counter = final_dest_counter + 1
				if not zumy_reach_num == zumy_numbers:
					final_dest_counter = 0
			is_in_form = True

		elif (formation_command in predef_unison_command):
			if not is_in_form:
				print("Error! Zumys are not in formation yet!")
				continue
			


		else:
			print("Error! Please only input predefined command.")



		# goal_pos = Pose2D()
		# goal_pos.x = input("Please input "+zumy_ID+"\'s x coord:")
		# goal_pos.y = input("Please input "+zumy_ID+"\'s y coord:")
		# goal_pos.theta = input("Please input "+zumy_ID+"\'s theta coord in deg:")
		# is_goal_reached = send_loc_req_stat(zumy_ID, goal_pos)

