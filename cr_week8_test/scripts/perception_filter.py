#!/usr/bin/env python
import rospy
from cr_week8_test.msg import human_info
from cr_week8_test.msg import object_info
from cr_week8_test.msg import perceived_info
import numpy as np

class perception:
    def __init__(self, perceived_info):
        self.id = 0
        self.object_size = 0
        self.human_action = 0
        self.human_expression = 0
        self.perceived_info = perceived_info

    def percept_filter(self, data):
        
        rospy.loginfo(rospy.get_caller_id() + "\n object heard \n%s", data) #publishing the message on terminal
        self.id = data.id 
        self.object_size = data.object_size #giving value to 
 
    def percept_filter1(self, data):
        #function that return the data(msg) from the human publisher
        rospy.loginfo(rospy.get_caller_id() + "\n human heard \n%s", data) #make log of generated msg 
    
        self.human_action = data.human_action #storing human action to variable    
        self.human_expression = data.human_expression #storing human_expression to variable

        self.variables() #randomly modifying the perceived vaiable
        self.publish_perceived_data(perceived_info)# publish data
        
    
    def variables(self):
        #function to modify the perceived variables
        value = int(np.random.uniform(1,8)) #generating random choice to assign 
        if value==1:
        #setting object_size to 0
            self.object_size = 0
        elif value==2:
        #setting human_action to 0
             self.human_action = 0
        elif value==3:
        #setting human_expression to 0
            self.human_expression = 0
        elif value==4:
        #setting object_size and human_action to 0
            self.object_size = 0
            self.human_action = 0
        elif value==5:
        #setting object_size and human_expression to 0
            self.object_size = 0
            self.human_expression = 0
        elif value==6:
        #setting human_action and human_expression to 0
            self.human_action = 0
            self.human_expression = 0
        elif value==7:
        #setting object_size, human_action and human_expression to 0
            self.object_size = 0 
            self.human_action = 0
            self.human_expression = 0
        elif random_choice==8:
        #no modifications required
            pass

    def publish_perceived_data(self, perceived_info):
        #publishing the perceived variables
        perceived_pub = rospy.Publisher('percievedInfo', perceived_info, queue_size=10)
    
        #updating perceieved params msg
        perceived_info_params = perceived_info()
        perceived_info_params.id = self.id
        perceived_info_params.object_size = self.object_size 
        perceived_info_params.human_action = self.human_action 
        perceived_info_params.human_expression = self.human_expression 

        perceived_pub.publish(perceived_info_params)#publishing perceived info message

        #generating log of publish message
        rospy.loginfo(perceived_info_params)
    

def perception_filter():
    rospy.init_node('perception_filter') #creating subscriber node
    
    percept = perception(perceived_info)
    
    #creating subscriber function that takes generated info as params
    rospy.Subscriber("objectInfo", object_info, percept.percept_filter) 
    rospy.Subscriber("humanInfo", human_info, percept.percept_filter1)  


    rospy.spin()

if __name__ == '__main__':
    perception_filter() #calling the subscriber node function


