#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

import threading

N_ROBOT = 3
N_STICK = 2

def vo_to_twist(vo):
  twist = Twist()
  twist.linear.x = vo[0]
  twist.angular.z = vo[1]
  return twist

class ManJoyState():
  def __init__(self):
    self.cmd_in = [(0,0)]*N_ROBOT
    self.joy_dest = range(N_STICK)
    self.joy_in = [(0,0)]*N_STICK
    self.lock = threading.Condition()

  def joy_callback(self, joy_msg):
    self.lock.acquire()
    # update joy_in based on analog axes
    self.joy_in[1] = (joy_msg.axes[1], joy_msg.axes[0])
    self.joy_in[0] = (joy_msg.axes[3], joy_msg.axes[2])
    
    # update desired destinations based on buttons
    buttons = []
    buttons.append([False,False,False,False])
    #buttons.append([joy_msg.axes[6] == 1, joy_msg.axes[7]==1, 
    #                joy_msg.axes[6] == -1, joy_msg.axes[7]== -1])
    buttons.append([joy_msg.buttons[12]==1, joy_msg.buttons[13]==1,
                    joy_msg.buttons[14]==1, joy_msg.buttons[15]==1])

    for d in range(N_STICK):
      if True in buttons[d]:
        dest = buttons[d].index(True) 
        self.joy_dest[d] = dest
        for d_other in range(N_STICK):
          if d_other is not d and self.joy_dest[d_other] is dest:
            self.joy_dest[d_other] = N_ROBOT
          
        rospy.loginfo('Set dest of stick %d to robot %d' % (d, self.joy_dest[d]))
    
    self.lock.release()

  def cmd_callback(self, which, tw_msg):
    self.lock.acquire()
    # update cmd_in
    self.cmd_in[which] = (tw_msg.linear.x, tw_msg.angular.z)
    rospy.loginfo('callback cmd_in[%d] = (%f,%f)' % 
      (which, self.cmd_in[which][0], self.cmd_in[which][1]))
    self.lock.release()
    
def talker():
  state = ManJoyState()

  rospy.init_node('man_joy_override', anonymous=True)

  pubs = []
  for i in range(N_ROBOT):
    pubs.append(rospy.Publisher('robot%d/cmd_vel' % i, Twist, queue_size = 1))
    
    # need to create a new functional scope to callback based on topic number
    def curried_callback(j):
      return lambda m: state.cmd_callback(j,m)

    rospy.Subscriber('robot%d/cmd_vel_in' % i, Twist, curried_callback(i))
  
  rospy.Subscriber('joy', Joy, state.joy_callback)
  r = rospy.Rate(30)

  while not rospy.is_shutdown():
    # for each publisher, use joystick if joy_dest designates one of the robots
    # otherwise use corresponding cmd_in
    for i in range(N_ROBOT):
      state.lock.acquire()
      which = i
      #rospy.loginfo('talker cmd_in[%d] = (%f,%f)' % 
        #(which, state.cmd_in[which][0], state.cmd_in[which][1]))

      if i in state.joy_dest:
        vo_cmd = state.joy_in[state.joy_dest.index(i)]
      else:
        vo_cmd = state.cmd_in[i]

      pubs[i].publish(vo_to_twist(vo_cmd))
      state.lock.release()

    r.sleep()

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException: pass
