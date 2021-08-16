import cv2 # ���������� ������������� ������
import numpy as np	# ���������� ��������������� �������������� �������
import video # ���������� ��� ������ � �������

if __name__ == '__main__':
    def nothing(*arg):
        pass
cv2.namedWindow( "video" ) # ������� ����� ������
cv2.namedWindow( "settings" ) # ������� ���� ��������
# ���������� ������
cap = video.create_capture(0)
# ������� 6 �������� ��� ��������� ���������� � ��������� ����� �������
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
    # ��������� �������� ��������
    h1 = cv2.getTrackbarPos('Hue_1', 'settings')
    s1 = cv2.getTrackbarPos('Saturation_1', 'settings')
    v1 = cv2.getTrackbarPos('Value_1', 'settings')
    h2 = cv2.getTrackbarPos('Hue_2', 'settings')
    s2 = cv2.getTrackbarPos('Saturation_2', 'settings')
    v2 = cv2.getTrackbarPos('Value_2', 'settings')
    # ��������� ��������� � �������� ���� �������
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    # ����������� ������ �� ���� � ������ HSV
    thresh = cv2.inRange(hsv, h_min, h_max)
	# ����������� ����
    cv2.imshow('video', video)
    cv2.imshow('settings', thresh) 
	# ���������� ������ ���������
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cap.release()
cv2.destroyAllWindows()
