#!/usr/bin/env python

import rospy
import random

from cr_week8_test.msg import robot_info
from cr_week8_test.msg import perceived_info
from cr_week8_test.srv import predict_robot_expression , predict_robot_expressionResponse
from bayesian.bbn import *



def controller(data):
	
	s=rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
        pub=rospy.Publisher('robot_info',robot_info,queue_size=10)     #initialising the publisher
        control= robot_info()  #defining the  variables
	
	server = s(data.object_size,data.human_action,data.human_expression)
	control.id = data.id
	control.p_happy=server.p_happy
	control.p_sad=server.p_sad
	control.p_neutral=server.p_neutral
	
        rospy.loginfo(control)  #display the messgae on the terminal
	pub.publish(control)    #publish the message 
	




def robot_controller():
	rospy.init_node('robot_controller')    #initializing the publisher node
	
	rospy.Subscriber("perceived_info", perceived_info,controller)   #subscribe to perceived_info 
	rospy.spin()




if __name__ == '__main__':
        try:
	        robot_controller()
	except rospy.ROSInterruptException:
		pass
