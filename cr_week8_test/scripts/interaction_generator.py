#!/usr/bin/env python

import rospy
import random
import numpy as np
from cr_week8_test.msg import object_info
from cr_week8_test.msg import human_info
#function to publish the message
def interaction_generator(): 
#defining a topic to which message will be published  
    pub = rospy.Publisher('objectInfo', object_info, queue_size=10)
    pub1 = rospy.Publisher('humanInfo', human_info, queue_size=10)
#initializing the publisher node and setting anonymous = True will append random integers at theend ofour publisher node
    rospy.init_node('Interaction_generator')
    rate= rospy.Rate(0.1)  #publishes at the rate of 10 message per second
    object1= object_info()
    human = human_info()
    id=1
    while not rospy.is_shutdown():
	object1.id= id
	object1.object_size= id
	human.id= round(np.random.uniform(1,3))
	human.human_expression= round(np.random.uniform(1,3))
        human.human_action= round(np.random.uniform(1,3))
	
	
	rospy.loginfo(object1)     #display the messgae on the terminal
	rospy.loginfo(human) 
	pub.publish(object1)       #publish the message
	pub1.publish(human) 
	rate.sleep()             #will wait enough enough untill the node publishes the message
	
	id += 1

if __name__ == '__main__':
    try:
        interaction_generator()
    except rospy.ROSInterruptException:  #capture the interruption signal
        pass
