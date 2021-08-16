#The program is executed in MUR IDE with a built-in underwater vehicle simulator

import cv2
import pymurapi as mur
import math
import time
auv = mur.mur_init()

x_center = 160
y_center = 120
speed = 15
flag = 0

def clamp(v, max_v, min_v):
        if v > max_v:
            return max_v
        if v < min_v:
            return min_v
        return v

def keep_depth(y_c,y_get):
	error_d = y_get - y_c
	power_d = error_d * 0.6
	power_d2 = clamp(power_d, 100, -100)
	power_d3 = clamp(power_d, 100, -100)
	auv.set_motor_power(2,-power_d2)
	auv.set_motor_power(3,-power_d3)
   	

def keep_yaw(x_c,x_get,sp):
	error_x = x_get - x_c
	power_x = error_x * 0.08
	power_d0 = clamp(power_x, 100, -100)
	power_d1 = clamp(power_x, 100, -100)
	auv.set_motor_power(0,clamp(speed+power_d0, 100, -100))
	auv.set_motor_power(1,clamp(speed-power_d1, 100, -100))

def stabization(x_center,x,y_center,y):
        error_y = y - y_center
        power_f = error_y * 0.2
        power_d0 = clamp(power_f, 100, -100)
        power_d1 = clamp(power_f, 100, -100)
        auv.set_motor_power(0,-power_d0)
        auv.set_motor_power(1,-power_d1)
        
        error_x = x - x_center 
        power_s = error_x * 0.5
        power_d4 = clamp(power_s, 100, -100)
        auv.set_motor_power(4,-power_d4)
        if (abs(error_y) <=1) and (abs(error_x) <=1):
            return True, True
        return False, False 

def	find_object(img,hsv1,hsv2,size):
    image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = hsv1
    hsv_max = hsv2
    image_bin = cv2.inRange(image_hsv,hsv_min,hsv_max)
    cv2.imshow("out_window", image_bin)
    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        for c in contours:   
                moments = cv2.moments(c)
                try:
                    x = int(moments['m10'] / moments['m00'])
                    y = int(moments['m01'] / moments['m00'])
                    if (moments['m00'] > size):
                        return True,x,y,True    
                    if (moments['m00'] > 100):
                        cv2.circle(img, (x, y), 10, (255,0,0), -1)
                        #cv2.drawContours( img, c, -1, (255,0,0), 3, -1 )
                        cv2.imshow("out_window1", img)
                        return True,x,y,False
                except ZeroDivisionError:
                    return False, 0, 0,False
    return False,0,0,False

def	find_object1(img,hsv1,hsv2):
    image_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = hsv1
    hsv_max = hsv2
    image_bin = cv2.inRange(image_hsv,hsv_min,hsv_max)
    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        for c in contours:   
            moments = cv2.moments(c)
            try:  
                if (moments['m00'] > 100):
                    return True
            except ZeroDivisionError:
                return False
    return False	

while True:
    image_f = auv.get_image_front()
    image_b = auv.get_image_bottom()

    if flag == 0:
        found,x,y,s_flag = find_object(image_f,(20,20,20),(40,255,255),20000)
        if found:
            keep_depth(y_center,y)
            keep_yaw(x_center,x,speed)
            if s_flag:
                flag+=1
                print("Step", flag, "done")
      else:
            auv.set_motor_power(0,5)
            auv.set_motor_power(1,-5)

    if flag ==1:
        found,x,y,s_flag = find_object(image_b,(0,50,50),(15,255,255),30000)
        if found:
            stab1,stab2 = stabization(x_center,x,y_center,y)
            if (stab1) and (stab2):
                stab1 = False
                stab2 = False
                flag+=1
                print("Step", flag, "done") 
        else:
            auv.set_motor_power(0,30)
            auv.set_motor_power(1,30)

    if flag == 2:
        found,x,y,s_flag  = find_object(image_f,(0,50,50),(15,255,255),10000)
        #found1 = find_object1(image_b,(120,10,10),(160,255,255))  
        if found:
            found1 = find_object1(image_b,(120,10,10),(160,255,255)) 
            speed =30
            keep_depth(y_center,y)
            keep_yaw(x_center,x,speed)
            if found1:
                flag+=1
                print("Step", flag, "done")
        else:
            auv.set_motor_power(0,5)
            auv.set_motor_power(1,-5)
   
    if flag ==3:
        found,x,y,s_flag = find_object(image_b,(120,10,10),(160,255,255),30000)
        if found:
            stab1,stab2 = stabization(x_center,x,y_center,y)
            if (stab1) and (stab2):
                stab1 = False
                stab2 = False    
                flag+=1
    if flag ==4:
        cv2.imshow("out_window1", image_b)
        auv.set_motor_power(2,50)
        auv.set_motor_power(3,50)
        if auv.get_depth()  < 0.3:         
            flag+=1
    if flag ==5:
        print('Good job simpleAUV')
        break
    ch = cv2.waitKey(50)
    if ch == 27:
        break
cv2.destroyAllWindows()
