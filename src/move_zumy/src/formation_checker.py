import math
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

def e_dist(del_x, del_y):
	return math.sqrt((del_x*del_x + del_y*del_y))

def getMin(x1, x2):
	if x1 > x2:
		return x2
	return x1

def getMax(x1,x2):
	if x1 > x2:
		return x1
	return x2

def getHDist(nparr_1, nparr_2):
	print nparr_1
	print nparr_2
	hausdorff_distance = getMax(directed_hDist(nparr_1, nparr_2), directed_hDist(nparr_2, nparr_1))
	print hausdorff_distance
	return hausdorff_distance

def directed_hDist(nparr_max, nparr_min):
	max_min_dist = sys.float_info.min
	for row1 in nparr_max:
		min_dist = sys.float_info.max
		for row2 in nparr_min:
			min_dist = getMin(e_dist(row1[0] - row2[0], row1[1] - row2[1]), min_dist)
		max_min_dist = getMax(min_dist, max_min_dist)
	return max_min_dist
		

def plotFormation(formation_array, centroid, mode):
	x_list = []
	y_list = []
	for row in formation_array:
		x_list.append(row[0])
		y_list.append(row[1])
	plt.clf()
	plt.plot(x_list, y_list, 'r*')

	fig = plt.gcf()
	circle_centroid=plt.Circle(centroid,0.01, color='g',fill=False)
	fig.gca().add_artist(circle_centroid)
	plt.axis([0,1.2,0,1.2])
	if mode:
		plt.draw()
		time.sleep(5)
	else:
		plt.show()

def getCentroid(formation_array):
	x_avg = 0.0
	y_avg = 0.0
	for row in formation_array:
		x_avg = x_avg + row[0]/len(formation_array)
		y_avg = y_avg + row[1]/len(formation_array)
	return (x_avg, y_avg)

def centerFormation(formation_array, centroid):
	for row in formation_array:
		row[0] = row[0] - centroid[0]
		row[1] = row[1] - centroid[1]

def main():
	interactive_mode = False
	np.set_printoptions(precision=3, suppress=True)
	if interactive_mode:
		plt.ion()
		plt.show()
	else:
		plt.ioff()
	
	formation_string = 't'
	if formation_string == 'h':
		coord = np.array([[0.1, 0.5, 90],
				[0.37, 0.5, 90],
				[0.63, 0.5, 90],
				[0.9, 0.5, 90]])
		coord2 = np.array([[0.1, 0.3, 90],
				[0.37, 0.3, 90],
				[0.63, 0.3, 90],
				[0.9, 0.3, 90]])
	if formation_string == 's':
		coord = np.array([[0.2, 0.2, 90],
				[0.8, 0.2, 90],
				[0.8, 0.8, 90],
				[0.2, 0.8, 90]])
		coord2 = np.array([[0.3, 0.3, 90],
				[0.9, 0.3, 90],
				[0.9, 0.9, 90],
				[0.3, 0.9, 90]])
	if formation_string == 't':
		coord = np.array([[0.76, 0.35, 90],
				[0.24, 0.35, 90],
				[0.5, 0.8, 90],
				[0.5, 0.5, 90]])
		coord2 = np.array([[0.76, 0.35, 90],
				[0.24, 0.35, 90],
				[0.5, 0.8, 90],
				[0.5, 0.5, 90]])
#		coord2 = np.array([[1.76, 0, 90],
#				[1.24, 0, 90],
#				[1.5, 0.45, 90],
#				[1.5, 0.15, 90]])
	if formation_string == 'd':
		coord = np.array([[0.7, 0.5, 90],
				[0.5, 0.2, 90],
				[0.3, 0.5, 90],
				[0.5, 0.8, 90]])
		coord2 = np.array([[0.7, 0.6, 90],
				[0.5, 0.3, 90],
				[0.3, 0.6, 90],
				[0.5, 0.9, 90]])
	if formation_string == 'v':
		coord = np.array([[0.5, 0.2, 90],
				[0.5, 0.5, 90],
				[0.5, 0.8, 90],
				[0.5, 1.1, 90]]) 
		coord2 = np.array([[0.3, 0.2, 90],
				[0.3, 0.5, 90],
				[0.3, 0.8, 90],
				[0.3, 1.1, 90]]) 

	result = checkFormation(coord, coord2, 0.08)
	print result

	#centroid = getCentroid(coord)
	#centroid2 = getCentroid(coord2)
	#print centroid
	#print centroid2

	#centerFormation(coord, centroid)
	#centerFormation(coord2, centroid2)
	#centroid = getCentroid(coord)
	#centroid2 = getCentroid(coord2)
	#print centroid
	#print centroid2

	#plotFormation(coord, centroid, interactive_mode)
	#plotFormation(coord2, centroid2, interactive_mode)
	return

def checkFormation(formation_goal_array, zumy_positions_array, error_threshold):
	centroid_goal = getCentroid(formation_goal_array)
	centroid_zumys = getCentroid(zumy_positions_array)
	centerFormation(formation_goal_array, centroid_goal)
	centerFormation(zumy_positions_array, centroid_zumys)

	hdist = getHDist(formation_goal_array, zumy_positions_array)

	if hdist > error_threshold:
		return False
	else:
		return True

main()



