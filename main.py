import cv2
import threading
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

counter = 0
face_match = False
reference_img = cv2.imread("ref.jpg")
if reference_img is None:
    print("Error: Unable to load reference image.")
else:
    print("Reference image loaded successfully.")

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img)['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

while True:
    ret, frame = cap.read()
    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
            counter += 1
        if face_match:
            cv2.putText(frame, 'Match!!', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Match!!', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
