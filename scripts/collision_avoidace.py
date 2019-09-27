#!/usr/bin/env python

import numpy as np
import rospy
import robot_dimensions as robo
from sensor_msgs.msg import PointCloud
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class CollisionAvoidance:

    def __init__(self):
        # Current velocity in x-direction and current angular velocity around the z-axis.
        self.current_vel_x = 0.0
        self.current_ang_z = 0.0

        # Maximum distance of obstacles to consider.
        # Todo: This should be dependent on the velocity.
        self.max_dist = 1

        # Subscribers to get the current velocity and the current readings of the laser scan.
        rospy.Subscriber("dead_reckoning", Odometry, self.velocity_callback)
        rospy.Subscriber("sonar_sensor", PointCloud, self.sonar_callback)

        # Publisher for the velocity adjustments calculated for collision avoidance.
        self.col_avoid_publisher = rospy.Publisher("collision_avoidance", Twist, queue_size=10)

        rospy.spin()

    def velocity_callback(self, current_odometry):
        self.current_vel_x = current_odometry.twist.twist.linear.x
        self.current_ang_z = current_odometry.twist.twist.angular.z

    def sonar_callback(self, current_sonar_scan):
        sonar_points = current_sonar_scan.points
        sonar_ranges = np.zeros(len(robo.sonar_angles))

        for i in range(0, len(robo.sonar_angles)):
            sonar_ranges[i] = np.sqrt(sonar_points[i].x**2 + sonar_points[i].y**2)

        # Calculate the velocity adjustment and publish it.
        c1= 1.0
        c2= 1.0
        force_mag = (np.clip(c1+c2*np.abs(np.cos(robo.sonar_angles))*np.abs(self.current_vel_x)/robo.max_vel)/sonar_ranges)**2
        force=np.zeros(2)
        for i in range(force_mag):
            force=force+force_mag[i]*np.array([np.cos(robo.sonar_angles[i]),np.sin(robo.sonar_angles[i])])

        non_holo_vel= np.arary([np.sqrt(force[0]**2+force[1]**2),np.arctan2(force[0],force[1])])

        velocity_adjustment = Twist()
        velocity_adjustment.linear.x = non_holo_vel[0]
        velocity_adjustment.angular.z = non_holo_vel[1]
        self.col_avoid_publisher.publish(velocity_adjustment)



if __name__ == '__main__':

    rospy.init_node("CollisionAvoidance")

    try:
        node = CollisionAvoidance()
    except rospy.ROSInterruptException:
        pass
