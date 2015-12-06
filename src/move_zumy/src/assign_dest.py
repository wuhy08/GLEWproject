#!/usr/bin/env python
import math
#import get_vel
import numpy as np
from itertools import permutations, combinations

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
	y_4 = end2[1]
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

def find_optimal_path_n(zumy_pos, final_dest):
	if zumy_pos.ndim == 2:
		zumy_number = np.shape(zumy_pos)[0]
	else:
		zumy_number = 1
		return final_dest
	pair_list = range(zumy_number)
	possible_pairs_iter = permutations(pair_list)
	possible_pairs = np.asarray([np.asarray(elem) for elem in possible_pairs_iter])
	pair_for_cross_iter = combinations(pair_list, 2)
	pair_for_cross = np.asarray([np.asarray(elem) for elem in pair_for_cross_iter])
	possible_total_distance = np.zeros(math.factorial(zumy_number))
	possible_cross = np.zeros(math.factorial(zumy_number))
	for ii in range(math.factorial(zumy_number)):
		current_pair = possible_pairs[ii]
		for jj in range(zumy_number):
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
	best_pair = possible_pairs[minimum_index]
	new_final_dest_tuple = tuple(final_dest[order] for order in best_pair)
	new_final_dest = np.vstack(new_final_dest_tuple)
	return new_final_dest


def array_func_test(func_name, args, ret_desired):
	ret_value = func_name(*args)
	if not isinstance(ret_value, np.ndarray):
		print('[FAIL] ' + func_name.__name__ + '() returned something other than a NumPy ndarray')
	elif ret_value.shape != ret_desired.shape:
		print('[FAIL] ' + func_name.__name__ + '() returned an ndarray with incorrect dimensions')
	elif not np.allclose(ret_value, ret_desired, rtol=1e-3):
		print('[FAIL] ' + func_name.__name__ + '() returned an incorrect value')
	else:
		print('[PASS] ' + func_name.__name__ + '() returned the correct value!')

def scalar_func_test(func_name, args, ret_desired):
	ret_value = func_name(*args)
	if (not isinstance(ret_value, float)) and (not isinstance(ret_value, int)):
		print('[FAIL] ' + func_name.__name__ + '() returned something other than a NumPy ndarray')
	elif not (ret_value-ret_desired)<=1e-3:
		print('[FAIL] ' + func_name.__name__ + '() returned an incorrect value')
	else:
		print('[PASS] ' + func_name.__name__ + '() returned the correct value!')

if __name__== '__main__':


	arg1 = np.array([3.5, 3.6])
	arg2 = np.array([6.2, 4.3])
	func_args = (arg1, arg2)
	ret_desired = 2.789
	scalar_func_test(get_distance, func_args, ret_desired)

	arg1 = np.array([0, 0])
	arg2 = np.array([1, 1])
	arg3 = np.array([1, 0])
	arg4 = np.array([0, 1])
	func_args = (arg1, arg2, arg3, arg4)
	ret_desired = 2
	scalar_func_test(check_crossing, func_args, ret_desired)
	#check_crossing(start1, end1, start2, end2):

	arg1 = np.array([0.5, 0.5])
	arg2 = np.array([0.9, 0.9])
	arg3 = np.array([2.28, 3.28])
	arg4 = np.array([4.28, 5.28])
	func_args = (arg1, arg2, arg3, arg4)
	ret_desired = 0
	scalar_func_test(check_crossing, func_args, ret_desired)
	#check_crossing(start1, end1, start2, end2):


	arg1 = np.array([0, 0.5])
	arg2 = np.array([0.7, 1])
	arg3 = np.array([0.53, 0])
	arg4 = np.array([1, 0.8])
	func_args = (arg1, arg2, arg3, arg4)
	ret_desired = 0
	scalar_func_test(check_crossing, func_args, ret_desired)
	#check_crossing(start1, end1, start2, end2):


	arg1 = np.array([0, 1])
	arg2 = np.array([0.5, 0.5])
	arg3 = np.array([0.53, 0])
	arg4 = np.array([1, 0.8])
	func_args = (arg1, arg2, arg3, arg4)
	ret_desired = 1
	scalar_func_test(check_crossing, func_args, ret_desired)
	#check_crossing(start1, end1, start2, end2):

	#Both inputs should be 4*3 np matrices
	arg1 = np.array([[0.42, 0.7, 90],
		[0.85, 0.32, 90],
		[0.05, 0.38, 90],
		[0.65, 0.44, 90]])
	arg2 = np.array([[0.1, 0.5, 90],
		[0.37, 0.5, 90],
		[0.63, 0.5, 90],
		[0.9, 0.5, 90]])
	func_args = (arg1, arg2)
	ret_desired = np.array([[0.37, 0.5, 90],
		[0.9, 0.5, 90],
		[0.1, 0.5, 90],
		[0.63, 0.5, 90]])
	array_func_test(find_optimal_path, func_args, ret_desired)
	#find_optimal_path(zumy_pos, final_dest)


	arg1 = np.array([[0.9, 0.5, 90],
		[0.7, 0.35, 90],
		[0.1, 0.4, 90],
		[0.35, 0.85, 90]])
	arg2 = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90],
				[0.8, 0.8, 90],
				[0.2, 0.8, 90]])
	func_args = (arg1, arg2)
	ret_desired = np.array([[0.8, 0.8, 90],
		[0.8, 0.2, 90],
		[0.2, 0.2, 90],
		[0.2, 0.8, 90]])
	array_func_test(find_optimal_path, func_args, ret_desired)
	#find_optimal_path(zumy_pos, final_dest)

	arg1 = np.array([[0.42, 0.7, 90],
		[0.85, 0.32, 90],
		[0.05, 0.38, 90],
		[0.65, 0.44, 90]])
	arg2 = np.array([[0.1, 0.5, 90],
		[0.37, 0.5, 90],
		[0.63, 0.5, 90],
		[0.9, 0.5, 90]])
	func_args = (arg1, arg2)
	ret_desired = np.array([[0.37, 0.5, 90],
		[0.9, 0.5, 90],
		[0.1, 0.5, 90],
		[0.63, 0.5, 90]])
	array_func_test(find_optimal_path_n, func_args, ret_desired)
	#find_optimal_path(zumy_pos, final_dest)


	arg1 = np.array([[0.9, 0.5, 90],
		[0.7, 0.35, 90],
		[0.1, 0.4, 90],
		[0.35, 0.85, 90]])
	arg2 = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90],
				[0.8, 0.8, 90],
				[0.2, 0.8, 90]])
	func_args = (arg1, arg2)
	ret_desired = np.array([[0.8, 0.8, 90],
		[0.8, 0.2, 90],
		[0.2, 0.2, 90],
		[0.2, 0.8, 90]])
	array_func_test(find_optimal_path_n, func_args, ret_desired)



	arg1 = np.array([[0.9, 0.5, 90],
		[0.1, 0.35, 90]])
	arg2 = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90]])
	func_args = (arg1, arg2)
	ret_desired = np.array([[0.8, 0.2, 90],
		[0.2, 0.2, 90]])
	array_func_test(find_optimal_path_n, func_args, ret_desired)