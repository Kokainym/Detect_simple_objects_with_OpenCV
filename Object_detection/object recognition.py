import cv2
import numpy as np
import math
import video

col = 4				#количество вершин у искомой фигуры
color_min = (45,50,50) 	#начальное значение диапазона цвета
color_max = (65,255,255)	#конечное значение диапазона цвета
area_min = 100			#минимальное значение площади
area_max = 3000		     #максимальное значение площади
#«ахват камеры
cap = video.create_capture(0)   
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
font = cv2.FONT_HERSHEY_COMPLEX
#‘ункци€ дл€ поиска объекта
def find_object(image,hsv1,hsv2):   
    low_hsv = np.array(hsv1, np.uint8)
    high_hsv = np.array(hsv2, np.uint8)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv,low_hsv, high_hsv) 
    c, hierarchy = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len© != 0:
        for c in contours:           
			moments = cv2.moments©
			try:      
				if (moments[Сm00Т] > area_min) and (moments[Сm00Т] < area_max):
					x = int(moments[Сm10Т]/ moments[Сm00Т])
					y = int(moments[Сm01Т] / moments[Сm00Т])                
					hull = cv2.convexHull©
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
		string = str(x) + У " + str(y)
		cv2.putText(image, string, (x+20, y),font, 0.5, (0, 255, 0))
		cv2.circle(image, (x, y), 10, (200, 0,0), -1)
    cv2.imshow('video', image)
    ch = cv2.waitKey(50)
    if ch == 27:
        break
cap.release()
cv2.destroyAllWindows()
