import cv2 # библиотека компьютерного зрения
import numpy as np	# библиотека высокоуровневых математических функций
import video # библиотека для работы с камерой

if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "video" ) # создаем видео потока
cv2.namedWindow( "settings" ) # создаем окно настроек
# подключаем камеру
cap = video.create_capture(0)
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('Hue_1', 'settings', 0, 255, nothing)
cv2.createTrackbar('Saturation_1', 'settings', 0, 255, nothing)
cv2.createTrackbar('Value_1', 'settings', 0, 255, nothing)
cv2.createTrackbar('Hue_2', 'settings', 255, 255, nothing)
cv2.createTrackbar('Saturation_2', 'settings', 255, 255, nothing)
cv2.createTrackbar('Value_2', 'settings', 255, 255, nothing)
crange = [0,0,0, 0,0,0]

while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV ) 
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('Hue_1', 'settings')
    s1 = cv2.getTrackbarPos('Saturation_1', 'settings')
    v1 = cv2.getTrackbarPos('Value_1', 'settings')
    h2 = cv2.getTrackbarPos('Hue_2', 'settings')
    s2 = cv2.getTrackbarPos('Saturation_2', 'settings')
    v2 = cv2.getTrackbarPos('Value_2', 'settings')
    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
	# отображение окон
    cv2.imshow('video', video)
    cv2.imshow('settings', thresh) 
	# завершение работы программы
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cap.release()
cv2.destroyAllWindows()
