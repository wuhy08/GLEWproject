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
		coord = np.array([[0.2, 0.5, 90],
				[0.4, 0.5, 90],
				[0.6, 0.5, 90],
				[0.8, 0.5, 90]])
	if formation_string == 's':
		coord = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90],
				[0.8, 0.8, 90],
				[0.2, 0.8, 90]])
	if formation_string == 't':
		coord = np.array([[0.5, 0.5, 90],
				[0.5, 0.8, 90],
				[0.24, 0.35, 90],
				[0.76, 0.35, 90]])
	if formation_string == 'd':
		coord = np.array([[0.5, 0.8, 90],
				[0.5, 0.2, 90],
				[0.3, 0.5, 90],
				[0.7, 0.5, 90]])
	if formation_string == 'v':
		coord = np.array([[0.5, 0.2, 90],
				[0.5, 0.4, 90],
				[0.5, 0.6, 90],
				[0.5, 0.8, 90]])
	return coord

def get_distance(coord1, coord2):
	distance = math.sqrt((coord2[1]-coord1[1])**2+(coord2[0]-coord1[0])**2)
	return distance

def check_crossing(start1, end1, start2, end2):
	x_1 = start1[0]
	y_1 = start1[1]
	x_2 = end1[0]
	y_2 = end1[1]
	x_3 = start2[0]
	y_3 = start2[1]
	x_4 = end2[0]
	x_4 = end2[1]
	A_1 = y_2 - y_1
	B_1 = x_1 - x_2
	C_1 = A_1*x_1 + B_1*y_1
	A_2 = y_4 - y_3
	B_2 = x_3 - x_4
	C_2 = A_2*x_3 + B_2*y_3
	det = A_1*B_2 - A_2*B_1
	if det == 0:
		return 0
	if not det == 0:
		x_cross = (B_2*C_1 - B_1*C_2)/det
		y_cross = (A_1*C_2 - A_2*C_1)/det
		delta_1 = -(x_cross-x_1)/B_1
		delta_2 = -(x_cross-x_3)/B_2
		cross_count = 0
		if delta_1>0 and delta_1<1:
			cross_count = cross_count + 1
		if delta_2>0 and delta_2<1:
			cross_count = cross_count + 1
		return cross_count


def find_optimal_path(zumy_pos, final_dest):
	possible_pairs = np.array([[0,1,2,3],
								[0,1,3,2],
								[0,2,1,3],
								[0,2,3,1],
								[0,3,1,2],
								[0,3,2,1],
								[1,0,2,3],
								[1,0,3,2],
								[1,2,0,3],
								[1,2,3,0],
								[1,3,0,2],
								[1,3,2,0],
								[2,0,1,3],
								[2,0,3,1],
								[2,1,0,3],
								[2,1,3,0],
								[2,3,0,1],
								[2,3,1,0],
								[3,0,1,2],
								[3,0,2,1],
								[3,1,0,2],
								[3,1,2,0],
								[3,2,0,1],
								[3,2,1,0]])
	pair_for_cross = np.array([[0,1],
								[0,2],
								[0,3],
								[1,2],
								[1,3],
								[2,3]])
	possible_total_distance = np.zeros(24)
	possible_cross = np.zeros(24)
	for ii in range(24):
		current_pair = possible_pairs[ii]
		for jj in range(4):
			possible_total_distance[ii] = possible_total_distance[ii] + \
					get_distance(zumy_pos[jj], final_dest[current_pair[jj]])
		for curr_pair_for_cross in pair_for_cross:
			possible_cross[ii] = possible_cross[ii] + \
					check_crossing(zumy_pos[curr_pair_for_cross[0]],
									final_dest[current_pair[curr_pair_for_cross[0]]],
									zumy_pos[curr_pair_for_cross[1]],
									final_dest[current_pair[curr_pair_for_cross[1]]])
	possible_total_penalty = 1000*possible_cross + possible_total_distance
	minimum_index = np.argmin(possible_total_penalty)
	new_final_dest = np.vstack((final_dest[possible_pairs[minimum_index, 0]],
								final_dest[possible_pairs[minimum_index, 1]],
								final_dest[possible_pairs[minimum_index, 2]],
								final_dest[possible_pairs[minimum_index, 3]]))
	return new_final_dest


if __name__== '__main__':
	is_goal_reached = True
	if not len(sys.argv) == 5:
		print('Wrong Number of Arguments!  We need to have 4 Zumys')
		sys.exit()
	zumy_ID = sys.argv[1:]
	zumy_monitor = {}
	for curr_zumy_ID in zumy_ID:
		zumy_monitor[curr_zumy_ID] = ZumyPosMonitor(curr_zumy_ID)

	predef_formation_command = ['h', 's', 't', 'd', 'v']
	while True:
		formation_command = raw_input("Please input formation command:")
		if formation_command in predef_formation_command:
			final_destination = translate_cmd_2_coord(formation_command)
			latest_zumy_pos = np.zeros((4,3))
			ii = 0
			for curr_zumy_ID in zumy_ID:
				latest_zumy_pos[ii] = np.array([zumy_monitor[curr_zumy_ID].position.x,
												zumy_monitor[curr_zumy_ID].position.y,
												zumy_monitor[curr_zumy_ID].position.theta])
			new_final_destination = find_optimal_path(latest_zumy_pos, final_destination)


		if not formation_command in predef_formation_command:
			print("Error! Please only input predefined command.")



		# goal_pos = Pose2D()
		# goal_pos.x = input("Please input "+zumy_ID+"\'s x coord:")
		# goal_pos.y = input("Please input "+zumy_ID+"\'s y coord:")
		# goal_pos.theta = input("Please input "+zumy_ID+"\'s theta coord in deg:")
		# is_goal_reached = send_loc_req_stat(zumy_ID, goal_pos)

