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

        cv2.imshow("Virtual Painter Window", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release_cap()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()