import cv2 # библиотека компьютерного зрения
import numpy # библиотека высокоуровневых математических функций
import math

# функция нахождения центра контура
def center ():
    moments = cv2.moments(cnt, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
    x = int(dM10 / dArea)
    y = int(dM01 / dArea)
    cv2.circle(img, (x, y), 5, (255,10,120), -1)
    string = str(x) + " " + str(y)
    cv2.putText(img, string, (x+20, y),font, 0.5, (0, 255, 0))
    return
# считываем изображение
img = cv2.imread('all.png')
font = cv2.FONT_HERSHEY_COMPLEX
# обработка изображения
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # конвертация в градации серого
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY) # перевод в одноканальное изображение
# Поиск замкнутых контуров
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) != 0:	
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if abs(area) < 200:
            continue
		#Нахождение количество вершин(переломов) в контуре
        hull = cv2.convexHull(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # треугольник
		if len(approx) == 3:           
            cv2.drawContours(img, [cnt], 0, (100, 140, 255), 3)
        # квадрат, приямоугольник
		if len(approx) == 4:           
            cv2.drawContours(img, [cnt], 0, (110, 140, 55), 3)            
        # пятиугольник
		if len(approx) == 5:           
            cv2.drawContours(img, [cnt], 0, (220, 123, 155), 3)
        # овал
		if len(approx) > 5:           
            cv2.drawContours(img, [cnt], 0, (120, 23, 55), 3)   
        # круг
		((_, _), (w, h), _) = cv2.minAreaRect(cnt) 
        (_, _), rad = cv2.minEnclosingCircle(cnt)
        r_area = w*h
        c_area = rad**2 * math.pi
        aspect_ratio = w/h
        if 0.9 <= aspect_ratio <= 1.1:
            if r_area > c_area:
                cv2.drawContours(img, [cnt], 0, (0, 140, 0), 3)
        center()
# вывод результата, завершение работы программы       
cv2.imshow('contours', thresh)
cv2.waitKey()
cv2.destroyAllWindows()
