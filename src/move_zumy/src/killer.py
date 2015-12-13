#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist

if __name__=='__main__':

	if len(sys.argv) < 3:
		print('Wrong Number of Arguments!  Use: killer.py [ zumy1 name ], [ zumy2 name ]')
		sys.exit()

	rospy.init_node('Killer')
	
	zumy1 = sys.argv[1]
	zumy2 = sys.argv[2]

	zumy_vel1 = rospy.Publisher('/%s/cmd_vel' % zumy1, Twist, queue_size=2)
	zumy_vel2 = rospy.Publisher('/%s/cmd_vel' % zumy2, Twist, queue_size=2)

	cmd = Twist()
	cmd.linear.x = 0
	cmd.linear.y = 0
	cmd.linear.z = 0
	cmd.angular.x = 0
	cmd.angular.y = 0
	cmd.angular.z = 0
	
	rate = rospy.Rate(100)

	while True:
		zumy_vel1.publish(cmd)
		zumy_vel2.publish(cmd)

		print 'KILLED'
		rate.sleep()

	rospy.spin()
