#!/usr/bin/python
import rospy
import sys
from BluetoothService import *
from bitstring import BitArray
from vibration_msgs.msg import VibrationArray

class hapticSnedNode(object):
    def __init__(self):
        self.node_name = rospy.get_name()

        self.enable = rospy.get_param('~bt', True)
        self.enable_bluetooth = self.enable
        self.mac = rospy.get_param('~mac', "98:D3:31:F4:0C:89")

        self.bt = BluetoothService()
        self.bluetooth_setup()

        self.frequencies = [0, 0, 0]
        self.intensities = [3, 3, 3]

        # Publicaiton
        
        # Subscriptions
        self.sub_vb_cmd = rospy.Subscriber("vibrate_cmd", VibrationArray, self.update, queue_size=1)

        # safe shutdown
        rospy.on_shutdown(self.custom_shutdown)

        # timer
        rospy.loginfo("[%s] Initialized " %(rospy.get_name()))
    
    def bluetooth_setup(self):

        self.toConnect = self.mac

        if self.enable_bluetooth:
            rospy.loginfo("Starting to connect bluetooth device (%s)" %(self.mac))
            self.bt.connect(self.toConnect,enablePrint=False)
        else:
            rospy.loginfo('Run without sending bt msg to arduino')

    def update(self, msg):
        #print msg.frequencies, msg.intensities
        if(self.frequencies != msg.frequencies or self.intensities != msg.intensities):
            self.frequencies = msg.frequencies
            self.intensities = msg.intensities
            self.send()

    def send(self):
        toSend = BitArray()
        for i in range(0,3):
            frequency = BitArray(uint=self.frequencies[i], length=3)
            intensity = BitArray(uint=self.intensities[i], length=3)
            state     = BitArray(uint=1, length=3)
            toSend.append(intensity)
            toSend.append(frequency)
            toSend.append(state)
        toSend.append('0b00000')
        toSend.append('0x00')
        if self.enable_bluetooth:
            rospy.loginfo("sending msg(hex): %s" %(toSend))
            rospy.loginfo("sending msg(bin): %s"%(toSend.bin))
            self.bt.send(self.toConnect, str(toSend.tobytes()))
        else:
            rospy.logdebug("sending msg: %s" %(toSend))
            rospy.logdebug(str(toSend.bin))

    def custom_shutdown(self):
        rospy.loginfo("[%s] Shutting down..." %self.node_name)

        # Send stop command
        self.frequencies = [0, 0, 0]
        self.intensities = [0, 0, 0]
        self.send()
        self.send()
        self.send()
        if self.enable_bluetooth:
            self.bt.disconnect(self.toConnect)

        rospy.loginfo("[%s] Shutdown" %self.node_name)

if __name__ == '__main__':
    rospy.init_node("haptic_send",anonymous=False)
    haptic_send_node = hapticSnedNode()
    rospy.spin()


