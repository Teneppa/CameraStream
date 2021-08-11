import cv2
cap = cv2.VideoCapture('http://10.0.0.115:5000/video_feed')

while True:
  ret, frame = cap.read()
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    exit(0)

