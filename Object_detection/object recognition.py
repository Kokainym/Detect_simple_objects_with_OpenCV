import cv2
import numpy as np
import math
import video

col = 4				#���������� ������ � ������� ������
color_min = (45,50,50) 	#��������� �������� ��������� �����
color_max = (65,255,255)	#�������� �������� ��������� �����
area_min = 100			#����������� �������� �������
area_max = 3000		     #������������ �������� �������
#������ ������
cap = video.create_capture(0)   
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
font = cv2.FONT_HERSHEY_COMPLEX
#������� ��� ������ �������
def find_object(image,hsv1,hsv2):   
    low_hsv = np.array(hsv1, np.uint8)
    high_hsv = np.array(hsv2, np.uint8)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv,low_hsv, high_hsv) 
    c, hierarchy = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len� != 0:
        for c in contours:           
			moments = cv2.moments�
			try:      
				if (moments[�m00�] > area_min) and (moments[�m00�] < area_max):
					x = int(moments[�m10�]/ moments[�m00�])
					y = int(moments[�m01�] / moments[�m00�])                
					hull = cv2.convexHull�
					peri = cv2.arcLength(c, True)
					 pprox. = cv2.approxPolyDP(c, 0.02 * peri, True)
					if len(approx) == col:           
						cv2.drawContours(image, [c], 0, (0, 140,0), 3)
						return True, x, y
			except ZeroDivisionError:
            return False,0,0
    return False,0,0

while True:
    flag, image = cap.read()
    found,x,y = find_object(image,color_min,color_max)
    if found:
		string = str(x) + � " + str(y)
		cv2.putText(image, string, (x+20, y),font, 0.5, (0, 255, 0))
		cv2.circle(image, (x, y), 10, (200, 0,0), -1)
    cv2.imshow('video', image)
    ch = cv2.waitKey(50)
    if ch == 27:
        break
cap.release()
cv2.destroyAllWindows()
