#!/usr/bin/python
import rospy
import sys
from BluetoothService import *
from bitstring import BitArray
from std_msgs.msg import String

class helloArduinoNode(object):
    """docstring for hapticControllerNode"""
    def __init__(self):
        self.node_name = rospy.get_name()

        self.enable_bluetooth = True
        self.mac = rospy.get_param('~mac', '98:D3:31:F4:0C:89')

        self.bt = BluetoothService()
        self.bluetooth_setup()

        if self.enable_bluetooth:
            self.bt.send(self.toConnect, 'hello arduino!')

        # Publicaiton
        
        # Subscriptions
        self.sub_bt_cmd = rospy.Subscriber("~bt_cmd", String, self.send_bt, queue_size=1)
        
        # safe shutdown
        rospy.on_shutdown(self.custom_shutdown)

        # timer
        rospy.loginfo("[%s] Initialized " %(rospy.get_name()))

        
    
    def bluetooth_setup(self):

        self.toConnect = self.mac

        if self.enable_bluetooth:
            self.bt.connect(self.toConnect,enablePrint=False)

    def send_bt(self, msg):
        
        if self.enable_bluetooth:
            self.bt.send(self.toConnect, msg.data)

    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)

        # Send stop command


        rospy.loginfo("[%s] Shutdown" %self.node_name)
if __name__ == '__main__':
    rospy.init_node("hello_arduino",anonymous=False)
    hello_arduino_node = helloArduinoNode()
    rospy.spin()

