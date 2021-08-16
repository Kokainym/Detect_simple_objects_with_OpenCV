#The program is executed in MUR IDE with a built-in underwater vehicle simulator

import cv2
import pymurapi as mur
import math
import time
import numpy as np
auv = mur.mur_init()

speed = 20
depth = 2.4
color_min = (20,50,50) 
color_max = (40,255,255)
x_center = 160
y_center = 120

def clamp(v, max_v, min_v):
        if v > max_v:
            return max_v
        if v < min_v:
            return min_v
        return v

def keep_depth(depth):
	error_d = auv.get_depth() - depth
	power_d = error_d * 70
	power_d2 = clamp(power_d, 100, -100)
	power_d3 = clamp(power_d, 100, -100)
	auv.set_motor_power(2,power_d2)
	auv.set_motor_power(3,power_d3)	

def	find_object(img,hsv1,hsv2):
	image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	hsv_min = hsv1
	hsv_max = hsv2
	image_bin = cv2.inRange(image_hsv,hsv_min,hsv_max)
	contours, _ = cv2.findContours(image_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	if contours:
		for c in contours:
			moments = cv2.moments(c)
			try:
				x = int(moments['m10']/ moments['m00'])
				y = int(moments['m01'] / moments['m00'])
				rect = cv2.minAreaRect(c)
				box = cv2.boxPoints(rect)
				box = np.int0(box) 
				center = (int(rect[0][0]),int(rect[0][1]))
				area = int(rect[1][0]*rect[1][1])
				edge1 = np.int0((box[1][0] - box[0][0],box[1][1] - box[0][1]))
				edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))            				
				usedEdge = edge1
				if cv2.norm(edge2) > cv2.norm(edge1):
					usedEdge = edge2
				reference = (1,0) 
				
				angle = 180.0/math.pi * math.acos((reference[0]*usedEdge[0] + reference[1]*usedEdge[1]) / (cv2.norm(reference) *cv2.norm(usedEdge))) 				
				cv2.putText(img, "%d" % int(angle), (x+50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,0,0), 2)
				cv2.drawContours(img,[box],0,(200,0,0),2)
				cv2.imshow("out_window", img)
				return True,x,y, angle 
			except ZeroDivisionError:
				return False, 0, 0, 0
	return False,0,0,0
	

while True:
	image = auv.get_image_bottom()
	
	found,x,y,angle = find_object(image,color_min,color_max)
	if found:
		keep_depth(depth)
		
		error_a = angle - 90
		power_a = error_a * 0.8
		power_d0 = clamp(power_a, 100, -100)
		power_d1 = clamp(power_a, 100, -100)
		auv.set_motor_power(0,clamp((speed-power_d0),100,-100))
		auv.set_motor_power(1,clamp((speed+power_d1),100,-100))
		time.sleep(0.4)
		error_y = y - y_center
		power_y = error_y * 6
		power_d00 = clamp(power_y, 100, -100)
		power_d11 = clamp(power_y, 100, -100)
		auv.set_motor_power(0,clamp((speed-power_d00),100,-100))
		auv.set_motor_power(1,clamp((speed+power_d11),100,-100))	
		error_x = x - x_center
		power_s = error_x * 0.5
		power_d4 = clamp(power_s, 60, -60)
		auv.set_motor_power(4,-power_d4)
		
	ch = cv2.waitKey(50)
	if ch == 27:
		break
cv2.destroyAllWindows()
