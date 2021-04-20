

import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


cap = cv2.VideoCapture(0)

scaleX = 1280
scaleY = 720

distance = 0
scale = 100
tempScale = 100

circleX = scaleX/2
circleY = 200

ballStatus = 0


def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)


def rescale_frame(frame, percent):
    global scaleX, scaleY
    scaleX = int(frame.shape[1] * percent / 100)
    scaleY = int(frame.shape[0] * percent / 100)
    dim = (scaleX, scaleY)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


change_res(scaleX, scaleY)


# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        scaleX = image.shape[1]
        scaleY = image.shape[0]
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
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        #                           #  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
        #                           #  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        #                           )

        leftHand = results.left_hand_landmarks
        rightHand = results.right_hand_landmarks

        def L(landmark):
            return leftHand.landmark[landmark]

        def R(landmark):
            return rightHand.landmark[landmark]

        def L_1F_CLOSE():
            return L(8).y > L(5).y

        def L_2F_CLOSE():
            return L(12).y > L(9).y

        def L_3F_CLOSE():
            return L(16).y > L(13).y

        def L_4F_CLOSE():
            return L(20).y > L(17).y

        def L_1F_2F_3F_4F_CLOSE():
            return L_1F_CLOSE() and L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()

        def R_1F_CLOSE():
            return R(8).y > R(5).y

        def R_2F_CLOSE():
            return R(12).y > R(9).y

        def R_3F_CLOSE():
            return R(16).y > R(13).y

        def R_4F_CLOSE():
            return R(20).y > R(17).y
        
        def R_1F_2F_3F_4F_CLOSE():
            return R_1F_CLOSE() and R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()

        def R_THUMB_OPEN():
            return R(4).x > R(3).x and R(3).x > R(2).x and R(4).x - R(5).x > R(5).x - R(13).x

        def L_THUMB_OPEN():
            return L(4).x < L(3).x and L(3).x < L(2).x and L(4).x - L(5).x < L(5).x - L(13).x

        def L_STOP():
            return L(8).y > L(5).y and L(12).y > L(9).y and L(16).y > L(13).y and L(20).y > L(17).y

        def R_STOP():
            return R(8).y > R(5).y and R(12).y > R(9).y and R(16).y > R(13).y and R(20).y > R(17).y

        def ZOOM_L():
            return L_THUMB_OPEN() and not L_1F_CLOSE() and L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()

        def ZOOM_R():
            return R_THUMB_OPEN() and not R_1F_CLOSE() and R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()
        # Left and Right

        def L_1F_OPEN():
            return not L_1F_CLOSE() and L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()

        def L_1F_2F_OPEN():
            return not L_1F_CLOSE() and not L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()

        def R_1F_OPEN():
            return not R_1F_CLOSE() and R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()

        def R_1F_2F_OPEN():
            return not R_1F_CLOSE() and not R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()

        def text(text, x, y, color=(255, 0, 0)):
            cv2.putText(image, text, (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, color)

        def drawCircle(x, y, color=(255, 0, 0)):
            # Center coordinates
            center_coordinates = (int(x), int(y))
            # Radius of circle
            radius = 20
            # Line thickness of 2 px
            thickness = 2
            cv2.circle(image, center_coordinates, radius, color, thickness)

        def MOVE_BALL(finger, thumb):
            global circleX, circleY, ballStatus
            drawCircle(finger(8).x*scaleX, finger(8).y*scaleY)
            if finger(8).x*scaleX - circleX < 10 and finger(8).y*scaleY - circleY < 10 and thumb():
                ballStatus = 1
            elif thumb() and ballStatus == 1:
                ballStatus = 0
            if finger(8).x*scaleX - circleX < 10 and finger(8).y*scaleY - circleY < 10 and not thumb() and ballStatus == 1:
                ballStatus = 2
            if ballStatus == 2:
                circleX = finger(8).x*scaleX
                circleY = finger(8).y*scaleY

        image = rescale_frame(image, percent=int(scale))
        # print(scaleX)

        if leftHand and rightHand:
            # Zoom
            if ZOOM_L() and ZOOM_R():
                zoom = 0
                if distance == 0:
                    tempScale = scale
                    distance = L(4).x-R(4).x
                else:
                    zoom = -(distance - (L(4).x-R(4).x))
                    scale = tempScale+int(zoom*100)
                text("Zoom: " + str(int(zoom*100)),
                     int(scaleX/2)-20, 300)
            else:
                distance = 0

            # Stop
            if L_1F_2F_3F_4F_CLOSE() and R_1F_2F_3F_4F_CLOSE():
                break

        if leftHand:
            if L_1F_OPEN():
                MOVE_BALL(L, L_THUMB_OPEN)
            else:
                ballStatus = 0
            

        if rightHand:
            if R_1F_OPEN():
                MOVE_BALL(R, R_THUMB_OPEN)
            else:
                ballStatus = 0

        drawCircle(circleX, circleY, (150, 100, 50))


        cv2.imshow('Raw Webcam Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
