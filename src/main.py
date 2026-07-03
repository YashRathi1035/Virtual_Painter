import cv2
from camera import Camera
from hand_tracker import HandTracker

def main():
    camera = Camera()
    tracker = HandTracker()

    while True:
        frame = camera.read_frame()

        if frame is None:
            break

        frame = tracker.hand_landmarks(frame)
        landmark_list = tracker.find_position(frame)

        if len(landmark_list) != 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(frame, str(landmark_list[8]), (50, 50), font, 1, (0, 0, 255), 2)
            if landmark_list:
                fingers = tracker.finger_up(landmark_list)
                
                if fingers == [0,1,0,0,0] or fingers == [1,1,0,0,0]:
                    cv2.putText(frame,"Draw Mode",(20,50),font,1,(0,0,255),2)
                elif fingers == [0,1,1,0,0] or fingers == [1,1,1,0,0]:
                    cv2.putText(frame,"Select Mode",(20,50),font,1,(0,0,255),2)
        
        cv2.imshow("Virtual Painter Window", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release_cap()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()