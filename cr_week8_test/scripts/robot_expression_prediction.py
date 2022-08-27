#!/usr/bin/env python

import rospy
import random
from cr_week8_test.msg import *
from cr_week8_test.srv import *
from bayesian.bbn import *
from bayesian.utils import make_key
from bayesian.exceptions import *

def f_objects(O):
	return 1.0/2.0

def f_humanaction(HA):
	return 1.0/3.0

def f_humanexpression(HE):
	return 1.0/3.0

def f_robotexpression(O, HA, HE, RE):
	if RE == '1':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.8
			elif O == '2':
				return 1
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.8
			elif O == '2':
				return 1
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.6
			elif O == '2':
				return 0.8
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.1
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.2

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.7
			elif O == '2':
				return 0.8
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.8
			elif O == '2':
				return 0.9
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.6
			elif O == '2':
				return 0.7
	
	if RE == '2':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.1
			elif O == '2':
				return 0.1
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.3
			elif O == '2':
				return 0.2
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.1
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.2
	if RE == '3':
		if HE == '1' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '1' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.0
		
		if HE == '2' and HA == '1':
			if O == '1':
				return 1.0
			elif O == '2':
				return 1.0
		if HE == '2' and HA == '2':
			if O == '1':
				return 0.9
			elif O == '2':
				return 0.8
		if HE == '2' and HA == '3':
			if O == '1':
				return 0.8
			elif O == '2':
				return 0.6

		if HE == '3' and HA == '1':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '3' and HA == '2':
			if O == '1':
				return 0.0
			elif O == '2':
				return 0.0
		if HE == '3' and HA == '3':
			if O == '1':
				return 0.2
			elif O == '2':
				return 0.1


def prediction(data):

	O = str(data.object_size)
	HA = str(data.human_action)
	HE = str(data.human_expression)

	robot_bbn = build_bbn(
		f_objects,
		f_humanaction,
		f_humanexpression,
		f_robotexpression,
		domains=dict(
			O = ['1', '2'],		
			HA = ['1', '2', '3'],
			HE = ['1', '2', '3'],
			RE = ['1', '2', '3']))	
	
	if O =='0' and HA == '0' and HE == '0':
		value = robot_bbn.query()
	elif O == '0' and HA == '0':
		value = robot_bbn.query(HE=HE)
	elif O == '0' and HE == '0':
		value = robot_bbn.query(HA=HA)
	elif HA == '0' and HE == '0':
		value = robot_bbn.query(O=O)
	elif HE == '0':
		value = robot_bbn.query(O=O, HA=HA)
	elif HA == '0':
		value = robot_bbn.query(O=O, HE=HE)
	elif O == '0':
		value = robot_bbn.query(HA=HE, HE=HE)

	perc = {n[1]:v for n,v in value.items() if n[0]=='RE'}	
	
	return predict_robot_expressionResponse(perc['1'], perc['2'], perc['3'])


def robot_expression_prediction():	
	rospy.init_node('robot_expression_prediction', anonymous=True)
	
	s = rospy.Service('predict_robot_expression', predict_robot_expression, prediction)
	
	rospy.spin()

if __name__ == '__main__':
	try:
		robot_expression_prediction()
	except rospy.ROSInterruptException:
		pass


