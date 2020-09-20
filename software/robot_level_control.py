'''
This module translates a robot level control velocity ( v_x and omega)
into axis level control velocities (v_1, v_2) for each wheel.
note that this is NOT the same as the turnrate for each wheel:
turnrate= v_i/(2*Pi*wheel-radius) for each wheel i.

theory:
v_x   = (v_1+v_2)/2
omega = (v_1-v_2)/(axis_length/2)
-> solving yields v_1 v_2
'''


import rospy
import sys
import numpy as np
import robot_dimensions as robo
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

#length of axis between both wheels [m]
def axis_level_control(twist):
    pub_left  = rospy.publisher("left_wheel_speed" ,Float32,queue_size=1)
    pub_right = rospy.publisher("right_wheel_speed",Float32,queue_size=1)
    v_x       = twist.linear.x
    omega     = twist.angular.z

    v_1 = Float32()
    v_2 = Float32()
    v_1 = v_x+(omega*robo.axis_length)/4
    v_2 = v_x-(omega*robo.axis_length)/4
    pub_left.publish(v_1)
    pub_right.publish(v_2)




if __name__=="__main__":
    try:
        rospy.init_node("robot_level_control")
        rospy.Subscriber(sys.argv[1],Twist,axis_level_control)
    except rospy.ROSInterruptException:
        rospy.loginfo("robot level control error")

