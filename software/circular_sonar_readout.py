#!/usr/bin/env python
'''
Reads each sonar Sensor in turn, calculates the distance and publishes all sensors via a pintcloud
slower than the regular one and meant as a temporary substitute
'''

import rospy
import numpy as np
import Jetson.GPIO as GPIO
import time
import robot_dimensions as robot
import threading
from std_msgs.msg import Header
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32





def distanz(pin_in,pin_out):
    # set Trigger on HIGH
    GPIO.output(pin_out, GPIO.HIGH)

    # set Trigger to LOW after 0.01ms
    time.sleep(0.00001)
    GPIO.output(pin_out, GPIO.LOW)

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(pin_in) == 0:
        StartZeit = time.time()

    while GPIO.input(pin_in) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distance = (TimeElapsed * 34300) / 2
    return distance


def sonar_sensing():
    Pros = []
    pub=rospy.Publisher("sonar_sensor",PointCloud,queue_size=10)
    GPIO.setmode(GPIO.BOARD)	
    GPIO.setup(robot.sonar_pins_in, GPIO.IN)
    GPIO.setup(robot.sonar_pins_out, GPIO.OUT)
    while not rospy.is_shutdown():
        output=PointCloud()
        header=Header()
        header.stamp=rospy.Time.now()
        header.frame_id="robot"
        output.header=header
        for i in range(8):
            sonar_reading=distanz(robot.sonar_pins_in[i],robot.sonar_pins_out[i])
            output.points.append(Point32(np.sin(robot.sonar_angles[i])*sonar_reading,np.cos(robot.sonar_angles[i])*sonar_reading,0 ))
        pub.publish(output)



if __name__=='__main__':
    try:
        barriers=[threading.Event() for _ in range(8)]
        global distances
        distances=np.zeros(8)
        rospy.init_node("Sonar")
        sonar_sensing()
    except rospy.ROSInterruptException:
        rospy.loginfo("sonar not working")
