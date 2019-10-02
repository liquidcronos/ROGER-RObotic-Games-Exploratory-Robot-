#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Header
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32


def laser_callback(current_laser_scan):
    real_angles   = np.array([-90.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 90.0])
    real_angles   = real_angles / 360.0 * 2 * np.pi
    opening_angle = 40.0/360.0*2*np.pi

    sensor_angles = np.arange(current_laser_scan.angle_min,
                              current_laser_scan.angle_max + current_laser_scan.angle_increment,
                              current_laser_scan.angle_increment)
    sensor_ranges = np.array(current_laser_scan.ranges)

    sonar_readings = np.zeros(len(real_angles))
    for i in range(len(real_angles)):
        sonar_readings[i]=np.min(sensor_ranges[np.where(np.logical_and(sensor_angles >= real_angles[i]-opening_angle/2,sensor_angles <= real_angles[i]+opening_angle/2))])
    
    pub=rospy.Publisher("robotic_games/sonar",PointCloud,queue_size=1)
    output=PointCloud()
    header=Header()
    header.stamp=rospy.Time.now()
    header.frame_id="robot"
    output.header=header
    for i in range(8):
        #TODO add position of Sensor on Pioneer!
        output.points.append((Point32(np.sin(real_angles[i])*sonar_readings[i],np.cos(real_angles[i])*sonar_readings[i],0  )))
    pub.publish(output)

def convert_laser_sonar():
    rospy.init_node("laser_to_sonar_conv")
    rospy.Subscriber("/p3dx/p3dx/laser/scan",LaserScan,laser_callback)
    rospy.spin()

if __name__=="__main__":
    try:
        convert_laser_sonar()
    except rospy.ROSInterruptException:
        pass

