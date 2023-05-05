import cv2
cap = cv2.VideoCapture("rtsp://10.5.3.119:554/test/Imeanit")

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()