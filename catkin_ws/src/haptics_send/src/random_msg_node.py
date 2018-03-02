#!/usr/bin/python
import rospy
import sys
from random import *
from bitstring import BitArray
from vibration_msgs.msg import VibrationArray

class randomMsgNode(object):
    """docstring for randomMsgNode"""
    def __init__(self):
        self.node_name = rospy.get_name()

        self.frequencies = [0, 0, 0]
        self.intensities = [3, 3, 3]

        # Publicaiton
        self.pub_vb_cmd =rospy.Publisher("vibrate_cmd", VibrationArray, queue_size=1)
        
        # Subscriptions

        # Publish without stop
        self.rate = rospy.Rate(1) # 1hz
        while not rospy.is_shutdown():
            # Random value
            self.frequencies = [randint(0,7),randint(0,7),randint(0,7)]
            self.intensities = [randint(1,5),randint(1,5),randint(1,5)]
            print "frequencies:",self.frequencies, "intensities:", self.intensities
            self.send()
            self.rate.sleep()

        # safe shutdown
        rospy.on_shutdown(self.custom_shutdown)

        # timer
        rospy.loginfo("[%s] Initialized " %(rospy.get_name()))

    def update_random(self, msg):
        print msg.frequencies, msg.intensities
        if(self.frequencies != msg.frequencies or self.intensities != msg.intensities):
            self.frequencies = msg.frequencies
            self.intensities = msg.intensities
            self.send()

    def send(self):
        vbArray = VibrationArray()
        vbArray.frequencies = self.frequencies
        vbArray.intensities = self.intensities
        self.pub_vb_cmd.publish(vbArray)

    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)

        # Send stop command
        self.frequencies = [0, 0, 0]
        self.intensities = [0, 0, 0]
        vbArray = VibrationArray()
        vbArray.frequencies = self.frequencies
        vbArray.intensities = self.intensities
        self.pub_vb_cmd.publish(vbArray)
        print self.frequencies, self.intensities
        self.pub_vb_cmd.publish(vbArray)
        print self.frequencies, self.intensities
        self.pub_vb_cmd.publish(vbArray)
        print self.frequencies, self.intensities
        self.rate.sleep()

        

        rospy.loginfo("[%s] Shutdown" %self.node_name)

if __name__ == '__main__':
    rospy.init_node("random_send",anonymous=False)
    random_send_node = randomMsgNode()
    rospy.spin()


