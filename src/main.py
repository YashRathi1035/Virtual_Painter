import cv2
from camera import Camera
from hand_tracker import HandTracker
import numpy as np

previous_x = 0
previous_y = 0

def main():
    camera = Camera()
    tracker = HandTracker()
    canvas = None

    while True:
        frame = camera.read_frame()

        if frame is None:
            break

        if canvas is None:
            canvas = np.zeros_like(frame)

        frame = tracker.hand_landmarks(frame)
        landmark_list = tracker.find_position(frame)

        if len(landmark_list) != 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(frame, str(landmark_list[8]), (50, 50), font, 1, (0, 0, 255), 2)
            if landmark_list:
                fingers = tracker.finger_up(landmark_list)
                index_x = landmark_list[8][1]
                index_y = landmark_list[8][2]
                
                if fingers == [0,1,0,0,0] or fingers == [1,1,0,0,0]:
                    cv2.putText(frame,"Draw Mode",(20,50),font,1,(0,0,255),2)

                    if previous_x == 0 and previous_y == 0:
                        previous_x = index_x
                        previous_y = index_y

                    cv2.line(canvas,(previous_x,previous_y),(index_x,index_y),(0,0,255),8)
                    previous_x = index_x
                    previous_y = index_y

                else:
                    previous_x = 0
                    previous_y = 0

                if fingers == [0,1,1,0,0] or fingers == [1,1,1,0,0]:
                    cv2.putText(frame,"Select Mode",(20,50),font,1,(0,0,255),2)
        
        frame = cv2.add(frame, canvas)
        cv2.imshow("Virtual Painter Window", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release_cap()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()