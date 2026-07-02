import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
    def read_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        return frame
    
    def release_cap(self):
        self.cap.release()