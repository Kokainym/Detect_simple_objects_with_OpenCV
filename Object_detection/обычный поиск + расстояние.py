import cv2
import pymurapi as mur
import math
import time
from videoserver import VideoServer
auv = mur.mur_init()
mur_view = VideoServer()
cap = cv2.VideoCapture(0)

x_center = 320
y_center = 180
speed = 0
color_min = (160,10,10) 
color_max = (180,255,255)
min_size = 500
max_size = 640*480
grani = 4
h = 150
f = 1

def clamp(v, max_v, min_v):
        if v > max_v:
            return max_v
        if v < min_v:
            return min_v
        return v

def keep_depth(y_c,y_get):
	error_d = y_get - y_c
	power_d = error_d * 0.5   
	power_d2 = clamp(power_d, 100, -100)
	power_d3 = clamp(power_d, 100, -100)
	auv.set_motor_power(0,-power_d2)
	auv.set_motor_power(3,-power_d3)	

def keep_yaw(x_c,x_get,sp):
	error_x = x_get - x_c
	power_x = error_x * 0.2
	power_d0 = clamp(power_x, 100, -100)
	power_d1 = clamp(power_x, 100, -100)
	auv.set_motor_power(1,clamp(speed+power_d0, 100, -100))
	auv.set_motor_power(2,clamp(speed-power_d1, 100, -100))

def distance (H):
    h = 60
    f = 3,04
    H_px = 480
    H_matrix = 2.76
    H = (H * H_matrix)/H_px
    d = (f*(H+h))/H
    return d

	
def	find_object(image,hsv1,hsv2,min_size,max_size):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_bin = cv2.inRange(image_hsv,color_min,color_max)
    mur_view.show(image_bin, 1)
    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        if len(contours) != 0:
                c = max(contours, key = cv2.contourArea)
                cv2.drawContours(image, [c], 0, (0, 250, 0), 3)
                hull = cv2.convexHull(c)
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if True:   
                    moments = cv2.moments(c)
                    try:
                        if (moments['m00'] > min_size) and (moments['m00'] < max_size):
                            x = int(moments['m10'] / moments['m00'])
                            y = int(moments['m01'] / moments['m00'])
                            x1, y1, w, h = cv2.boundingRect(c)
                            cords = str(x) + " " + str(y)
                            cv2.putText(image, cords, (x+50, y),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                            cv2.putText(image, str(moments['m00']), (x-150, y),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                            cv2.putText(image, str(h), (60, 60),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 240, 255))
                            return True,x,y,h
                        if moments['m00'] > max_size:                            
                            auv.set_rgb_color(255, 0, 0)
                            return False, 0, 0, 0 
                    except ZeroDivisionError:
                        return False, 0, 0, 0
    auv.set_rgb_color(0, 0, 255)
    return False,0,0, 0
	

while True:
    ret, image = cap.read()
    found,x,y,H = find_object(image,color_min,color_max,min_size,max_size)
    mur_view.show(image, 0)
    
    if found:
        auv.set_rgb_color(0, 255, 0)
        
        dist = distance(H)
        print (dist) 
        #cv2.putText(image, str(H), (60, 60),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 240, 255))
        
    


