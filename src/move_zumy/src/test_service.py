#!/usr/bin/env python

import rospy
import sys
import math
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import numpy as np

import matplotlib.pyplot as plt

from move_zumy.srv import AStarSolver

import matplotlib.patches as patches

if __name__== '__main__':

    width = 120
    height = 120

    zumy_width = 10.0/width
    zumy_height = 10.0/height

    pose_start = Pose2D(0.80, 0.49, -88.8)
    pose_goal = Pose2D(0.05, 0.53, 0)

    zumy1 = Pose2D(0.47, 0.48, 0.0) # Obstacle

    rospy.init_node('test_service_node')
    
    rospy.wait_for_service('astar_solver')

    astar = rospy.ServiceProxy('astar_solver', AStarSolver)
    # print astar([zumy1, zumy2], pose_start, pose_goal)
    response = astar([zumy1], pose_start, pose_goal)
    path = response.path

    # plt.ion()
    # plt.show()

    # plt.clf()

    fig = plt.figure()

    ax1 = fig.add_subplot(111, aspect='equal')
    ax1.add_patch(
        patches.Rectangle(
            (zumy1.x, zumy1.y),   # (x,y)
            zumy_width,          # width
            zumy_height,          # height
        )
    )

    xs = list(map(lambda p: p.x, path))
    ys = list(map(lambda p: p.y, path))

    ax1.plot(xs, ys, 'ro')
    ax1.set_xlim([0, 1.0])
    ax1.set_ylim([0, 1.0])

    # ax1.plot([3,4,-1,-4])
    plt.show()

    # plt.draw()

    # name = 'zumyBML3'
    # test_pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=2, latch=True)
    # the_speed = Twist()
    # rate = rospy.Rate(0.001)
    # the_speed.linear.x = float(sys.argv[1])
    # the_speed.linear.y = 0
    # the_speed.linear.z = 0
    # the_speed.angular.x = 0
    # the_speed.angular.y = 0
    # the_speed.angular.z = 0

    # while not rospy.is_shutdown():
    #     test_pub.publish(the_speed)
    #     rate.sleep()
