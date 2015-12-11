#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist

if __name__  == '__main__':
	rospy.init_node("test_pub")
	test_pub = rospy.Publisher('/zumyBML3/cmd_vel', Twist,queue_size = 5)
	rate = rospy.Rate(0.1)
	while True:
		right_vel = raw_input("give me velocity")
		right_vel = float(right_vel)
		test_pub_data = Twist()
		test_pub_data.angular.z = right_vel
		test_pub.publish(test_pub_data)
		rate.sleep()
