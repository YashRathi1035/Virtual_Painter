import cv2
from camera import Camera
from hand_tracker import HandTracker
import numpy as np


def main():
    previous_x = 0
    previous_y = 0

    brush_color = (255, 0, 255)
    small_brush = 5
    medium_brush = 10
    large_brush = 20
    brush_thickness = medium_brush
    brush_menu_open = False

    eraser_thickness = 40
    toolbar_height = 100

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

        h, w, _ = frame.shape
        
        

        if len(landmark_list) != 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(frame, str(landmark_list[8]), (50, 50), font, 1, (0, 0, 255), 2)

            fingers = tracker.finger_up(landmark_list)
            index_x = landmark_list[8][1]
            index_y = landmark_list[8][2]
                
            if fingers == [0,1,0,0,0] or fingers == [1,1,0,0,0]:
                cv2.putText(frame,"Draw Mode",(20,50),font,1,(0,0,255),2)

                if previous_x == 0 and previous_y == 0:
                    previous_x = index_x
                    previous_y = index_y

                if index_y > toolbar_height:
                    cv2.line(canvas,(previous_x,previous_y),(index_x,index_y),
                            brush_color,brush_thickness)
                previous_x = index_x
                previous_y = index_y

            elif fingers == [0,1,1,0,0] or fingers == [1,1,1,0,0]:
                previous_x = 0
                previous_y = 0
                index_x = landmark_list[8][1]
                index_y = landmark_list[8][2]

                if index_y < toolbar_height:
                    if 20 < index_x < 80:
                        brush_color = (0, 0,255)
                    elif 100 < index_x < 160:
                        brush_color = (255,0,0)
                    elif 180 < index_x < 240:
                        brush_color = (0,255,0)
                    elif 260 < index_x < 320:
                        brush_color = (0,255,255)
                    elif 340 < index_x < 400:
                        brush_color = (0,0,0)
                    elif 420 < index_x < 480:
                        canvas = np.zeros_like(frame)
                    elif 500 < index_x < 560:
                        brush_menu_open = True

                if brush_menu_open:
                    if 110 < index_y < 150:
                        if 380 < index_x < 420:
                            brush_thickness = small_brush
                            brush_menu_open = False
                        elif 440 < index_x < 480:
                            brush_thickness = medium_brush
                            brush_menu_open = False
                        elif 500 < index_x < 540:
                            brush_thickness =large_brush
                            brush_menu_open = False

                cv2.putText(frame,"Select Mode",(20,50),font,1,(0,0,255),2)

        else:
            previous_x = 0
            previous_y = 0
        
        frame = cv2.add(frame, canvas)
        ## Toolbar
        cv2.rectangle(frame, (0,0), (w,toolbar_height),(50,50,50), -1)

        ## Red
        cv2.rectangle(frame, (20,20), (80,80), (0,0,255), -1)
        ## Blue
        cv2.rectangle(frame, (100,20), (160,80), (255,0,0), -1)
        ## Green
        cv2.rectangle(frame, (180,20), (240,80), (0,255,0), -1)
        ## Yello
        cv2.rectangle(frame, (260,20), (320,80), (0,255,255), -1)
        ## Eraser
        cv2.rectangle(frame, (340,20), (400,80), (255,255,255), -1)
        cv2.putText(frame, "E", (360,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        ## Clear
        cv2.rectangle(frame, (420,20), (480,80), (150,150,150), -1)
        cv2.putText(frame, "C", (440,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        ## Brush Thickness
        cv2.rectangle(frame, (500,20), (560,80), (150,150,150), -1)
        cv2.putText(frame, "BT", (520,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

        if brush_menu_open == True:
            cv2.rectangle(frame,(360,100),(560,160),(50,50,50),-1)
            cv2.rectangle(frame,(380,110),(420,150),(150,150,150),-1)
            cv2.putText(frame,"1",(390,140),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            cv2.rectangle(frame,(440,110),(480,150),(150,150,150),-1)
            cv2.putText(frame,"2",(450,140),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            cv2.rectangle(frame,(500,110),(540,150),(150,150,150),-1)
            cv2.putText(frame,"3",(510,140),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

        cv2.circle(frame, (600, 50), 20, brush_color, -1)

        cv2.imshow("Virtual Painter Window", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):
            canvas[:] = 0
        if key == ord('q'):
            break

    camera.release_cap()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()