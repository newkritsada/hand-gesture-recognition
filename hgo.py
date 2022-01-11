
import cube
import mediapipe as mp
import cv2
from threading import Thread

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/cube.py')

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

scaleX = 1280
scaleY = 720
# windowX = 200
# windowY = 200
tempWindowX = 200
tempWindowY = 200

cap.set(3, scaleX)
cap.set(4, scaleY)
frame = cap.read()

# Hand Gesture
leftHand = None
rightHand = None

# Zoom
distance = 0
tempScale = 100

scaleInit = 0
scale = 100
tempScaleWindow = 100

# Rotate
rotateXStartL = 0
rotateYStartL = 0
rotateXStartR = 0
rotateYStartR = 0
tempRotateXStartL = 0
tempRotateYStartL = 0
tempRotateXStartR = 0
tempRotateYStartR = 0


def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)


def rescale_frame(frame, percent=100):
    global scaleX, scaleY
    scaleX = int(frame.shape[1] * percent / 100)
    scaleY = int(frame.shape[0] * percent / 100)
    dim = (scaleX, scaleY)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


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

    # Action


def L_STOP():
    return L(8).y > L(5).y and L(12).y > L(9).y and L(16).y > L(13).y and L(20).y > L(17).y


def R_STOP():
    return R(8).y > R(5).y and R(12).y > R(9).y and R(16).y > R(13).y and R(20).y > R(17).y


def ZOOM_L():
    return L_THUMB_OPEN() and not L_1F_CLOSE() and L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()


def ZOOM_R():
    return R_THUMB_OPEN() and not R_1F_CLOSE() and R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()


def RE_SCALE_L():
    return L_THUMB_OPEN() and not L_1F_CLOSE() and not L_2F_CLOSE() and not L_3F_CLOSE() and not L_4F_CLOSE()

def RE_SCALE_R():
    return R_THUMB_OPEN() and not R_1F_CLOSE() and not R_2F_CLOSE() and not R_3F_CLOSE() and not R_4F_CLOSE()


def L_1F_OPEN():
    return not L_1F_CLOSE() and L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()


def L_1F_2F_OPEN():
    return not L_1F_CLOSE() and not L_2F_CLOSE() and L_3F_CLOSE() and L_4F_CLOSE()


def R_1F_OPEN():
    return not R_1F_CLOSE() and R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()


def R_1F_2F_OPEN():
    return not R_1F_CLOSE() and not R_2F_CLOSE() and R_3F_CLOSE() and R_4F_CLOSE()


def hand_gesture_main():
    # global windowX, windowY
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX, windowY)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        global frame
        global scale,scaleInit,tempScaleWindow
        global scaleX, scaleY
        global leftHand, rightHand

        while cap.isOpened():
            

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            scaleX = image.shape[1]
            scaleY = image.shape[0]
            leftHand = results.left_hand_landmarks
            rightHand = results.right_hand_landmarks

            # 2. Right hand
            mp_drawing.draw_landmarks(
                image, rightHand, mp_holistic.HAND_CONNECTIONS)

            # 3. Left Hand
            mp_drawing.draw_landmarks(
                image, leftHand, mp_holistic.HAND_CONNECTIONS)

            def text(text, x, y, color=(255, 0, 0)):
                cv2.putText(image, text, (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, color)

            def drawCircle(x, y, color=(255, 0, 0), radius=20):
                # Center coordinates
                center_coordinates = (int(x), int(y))
                # Radius of circle
                # radius = 20
                # Line thickness of 2 px
                thickness = 2
                cv2.circle(image, center_coordinates, radius, color, thickness)

            image = rescale_frame(image,scale)

            # print(scaleX)
            global distance
            global rotateXStartL, rotateYStartL, rotateXStartR, rotateYStartR
            if leftHand and rightHand:

                # Zoom
                if ZOOM_L() and ZOOM_R():
                    zoom = 0
                    if distance == 0:
                        # ballScaleTemp = ballScale
                        distance = L(4).x-R(4).x
                    else:
                        zoom = -(distance - (L(4).x-R(4).x))
                        # print(zoom)
                        zoom = zoom/5
                        cube.Zoom(1+zoom, 1+zoom, 1+zoom)

                    text("Zoom: " + str(int(zoom*100)), 10, 300)
                else:
                    cube.ZOOM = False
                    distance = 0

                if RE_SCALE_L() and RE_SCALE_R():
                    zoom = 0
                    if scaleInit == 0:
                        # ballScaleTemp = ballScale
                        scaleInit = L(4).x-R(4).x
                        tempScaleWindow = scale
                    else:
                        zoom = -(scaleInit - (L(4).x-R(4).x))
                        if not scale+int(zoom*100) <= 10:
                            scale = tempScaleWindow+int(zoom*100)
                        

                    text("Re Scale: " + str(int(zoom*100)), 10, 300)
                else:

                    scaleInit = 0

                # Stop
                if L_1F_2F_3F_4F_CLOSE() and R_1F_2F_3F_4F_CLOSE():
                    cube.Stop()
                    break

            if leftHand:
                text("RIGHT HAND", scaleX-400, 100)

                if L_1F_2F_OPEN():
                    drawCircle(L(12).x*scaleX, L(12).y*scaleY)
                    # slide = 0
                    vX = 0
                    vY = 0
                    if rotateXStartL == 0 and rotateYStartL == 0:
                        rotateXStartL = int(L(12).x*50)
                        rotateYStartL = int(L(12).y*50)
                    else:
                        if rotateXStartL != int(L(12).x*50):
                            vX = int(L(12).x*50)-rotateXStartL
                            rotateXStartL = int(L(12).x*50)
                        else:
                            vX = 0
                        if rotateYStartL != int(L(12).y*50):
                            vY = int(L(12).y*50)-rotateYStartL
                            rotateYStartL = int(L(12).y*50)
                        else:
                            vY = 0
                        print(vX, vY)
                        print("start = ", rotateXStartL, rotateYStartL)
                        cube.Rotate(vX, vY)

                else:
                    cube.ROTATE = False

            if rightHand:
                text("LEFT HAND", 1, 100)

                if R_1F_2F_OPEN():
                    drawCircle(R(12).x*scaleX, R(12).y*scaleY)

                    vX = 0
                    vY = 0
                    if rotateXStartR == 0 and rotateYStartR == 0:
                        rotateXStartR = int(R(12).x*50)
                        rotateYStartR = int(R(12).y*50)
                    else:
                        if rotateXStartR != int(R(12).x*50):
                            vX = int(R(12).x*50)-rotateXStartR
                            rotateXStartR = int(R(12).x*50)
                        else:
                            vX = 0
                        if rotateYStartR != int(R(12).y*50):
                            vY = int(R(12).y*50)-rotateYStartR
                            rotateYStartR = int(R(12).y*50)
                        else:
                            vY = 0
                        print(vX, vY)
                        print("start = ", rotateXStartR, rotateYStartR)
                        cube.Rotate(vX, vY)

                else:
                    cube.ROTATE = False

            # drawCircle(circleX, circleY, (150, 100, 50), ballScale)

            cv2.imshow('Raw Webcam Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cube.Stop()
                break

        cap.release()
        cv2.destroyAllWindows()

def init():
    cube.width = scaleX
    cube.height = scaleY

    # video_thread = Thread(target=hand_gesture_main, args=())
    video_thread = Thread(target=cube.Main, args=())
    video_thread.start()

def run():
    cube.Main()


init()
hand_gesture_main()
# run()

