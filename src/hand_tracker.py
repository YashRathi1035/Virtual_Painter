import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self,detection_confidence=0.7,tracking_confidence=0.7,max_hands=1):
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.max_hands=max_hands

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = max_hands,
            min_detection_confidence = detection_confidence,
            min_tracking_confidence = tracking_confidence
        )
        self.result = None

    def hand_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgb)

        if self.result.multi_hand_landmarks:
            for hand_landmark in self.result.multi_hand_landmarks:
                if True:
                    self.mp_drawing.draw_landmarks(frame, hand_landmark, self.mp_hands.HAND_CONNECTIONS)

        return frame
    
    def find_position(self, frame, hand_no=0, draw = True):
        landmark_list = []

        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[hand_no]
            h, w, c = frame.shape

            for id, landmark in enumerate(my_hand.landmark):
                cx = int(landmark.x * w)
                cy = int(landmark.y * h)

                landmark_list.append([id, cx, cy])

                if draw:
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                    

        return landmark_list
    
    def finger_up(self, landmark_list):
        fingers = []

        if landmark_list[4][1] > landmark_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        tip_id = [8, 12, 16, 20]

        for tip in tip_id:
            if landmark_list[tip][2] < landmark_list[tip-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers