# hcc-lab4
haptic-device using PC(ROS) and Arduino

## Installation

### Dependencies

```
sudo apt-get install python-bluetooth python-pip bluez bluetooth
sudo pip install bitstring
```
### ROS Package

```
$ git clone https://github.com/OpenPPAT/hcc-lab4.git
$ cd hcc-lab4
$ source environment.sh
$ cd catkin_ws
$ catkin_make
```
## Run the Examples
terminal 1
```
$ roscore
```
terminal 2
```
$ rosrun rosrun hello_arduino hello_arduino.py idx:=[mac address] 
```
