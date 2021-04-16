

import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


cap = cv2.VideoCapture(0)

width = 1280
height = 720


def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


change_res(width, height)

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)

        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw face landmarks
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)

        # 1. Draw face landmarks
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
        #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
        #                          mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
        #                          )

        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  #  mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                  #  mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                  )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  #  mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                  #  mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                  )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  #  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                  #  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                  )




        leftHand = results.left_hand_landmarks
        rightHand = results.right_hand_landmarks

        # Left and Right
        if leftHand and rightHand:
            cv2.putText(image, "Right Hand", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            cv2.putText(image, "Left Hand", (width-200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

            dis = leftHand.landmark[20].x-rightHand.landmark[20].x
            cv2.putText(image, str(dis) , (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0))
            image = rescale_frame(image, percent=dis*100)
            

        # Left
        if leftHand:
            cv2.putText(image, "Left Hand", (width-200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            # stop
            if leftHand.landmark[8].y > leftHand.landmark[5].y and leftHand.landmark[12].y > leftHand.landmark[9].y and leftHand.landmark[16].y > leftHand.landmark[13].y and leftHand.landmark[20].y > leftHand.landmark[17].y:
                break



        # Right
        if rightHand:
            cv2.putText(image, "Right Hand", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.imshow('Raw Webcam Feed', image)



        



        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
