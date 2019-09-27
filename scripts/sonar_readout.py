'''
Reads each sonar Sensor, calculates the distance and publishes all sensors via a pintcloud
'''


import Jetson.GPIO as GPIO
import time
import robot_dimensions as robot
from multiprocessing import Process
from sensor_msgs.msg import PointCloud

def distanz(pin_in,pin_out):
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(pin_out, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(pin_in) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(pin_in) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz


def sonar_sensing():
    Pros = []
    while not rospy.is_shutdown():
        # actiave only 4 sensors at a time to avoid crossdetection
        odd_distance=np.zeros(4)
        for i in range(4):
        


if__name__=='__main__':
    try:
        rospy.init_node("Sonar")
        pub=rospy.Publisher("Sonar_sensor",PointCloud,queue_size=10)
        sonar_sensing()
    except rospy.ROSInterruptException:
        rospy.loginfo("sonar not working")
