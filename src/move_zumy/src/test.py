#!/usr/bin/env python
import rospy
import sys
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import numpy as np

if __name__== '__main__':
	rospy.init_node('send_speed_test')
	name = 'zumyBML3'
	test_pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=2, latch=True)
	the_speed = Twist()
	rate = rospy.Rate(0.001)
	the_speed.linear.x = float(sys.argv[1])
	the_speed.linear.y = 0
	the_speed.linear.z = 0
	the_speed.angular.x = 0
	the_speed.angular.y = 0
	the_speed.angular.z = 0
	while not rospy.is_shutdown():
		test_pub.publish(the_speed)
		rate.sleep()
