# shape_predictor_68_face_landmarks.dat
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import csv

data_set = "shape_predictor_68_face_landmarks.dat"
EYE_AR_THRESH = 0.27
EYE_AR_CONSEC_FRAMES = 3


def save_position(direction, total_Frames, array):
    temp = str(direction) + "-" + str(int(total_Frames/30))
    array.append(temp)


def create_names(code, number):
    names = []
    if number == 0:
        for i in range(len(code)):
            videofileM = str(code[i]) + 'M.mp4'
            videofileV = str(code[i]) + 'V.mp4'
            names.append(videofileM)
            names.append(videofileV)
    else:
        for i in range(len(code)):
            videofile = str(code[i]) + '.mp4'
            names.append(videofile)

    return names


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
in_loop = True


def blinkCounter(video):
    directions = []
    TOTAL = 0
    COUNTER = 0
    Total_Frames = 0
    time_for_blink = []
    consecutive_frames = []
    print("starting blink detection on: ", video)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(data_set)
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    vs = FileVideoStream(video).start()
    fileStream = True
    time.sleep(1.0)
    while in_loop:
        if fileStream and not vs.more():
            return TOTAL, Total_Frames, time_for_blink, directions

        frame = vs.read()
        Total_Frames += 1
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                consecutive_frames.append(Total_Frames)
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    if len(consecutive_frames) != 0:
                        timeStamp = consecutive_frames[0] / 30
                        time_for_blink.append(int(timeStamp))
                consecutive_frames = []
                COUNTER = 0
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return TOTAL, Total_Frames, time_for_blink, directions
        if key == ord("7"):
            print("Upper Left")
            save_position("UL", Total_Frames, directions)
        if key == ord("8"):
            print("Up")
            save_position("U", Total_Frames, directions)
        if key == ord("9"):
            print("Upper Right")
            save_position("UR", Total_Frames, directions)
        if key == ord("4"):
            print("left")
            save_position("L", Total_Frames, directions)
        if key == ord("5"):
            print("middle")
            save_position("M", Total_Frames, directions)
        if key == ord("6"):
            print("right")
            save_position("R", Total_Frames, directions)
        if key == ord("1"):
            print("down left")
            save_position("DL", Total_Frames, directions)
        if key == ord("2"):
            print("down")
            save_position("D", Total_Frames, directions)
        if key == ord("3"):
            print("down right")
            save_position("DR", Total_Frames, directions)

    cv2.destroyAllWindows()
    vs.stop()


def save_blinks(video):
    sex = input('choose sex (M | F): ')
    if sex == 'm' or sex == 'M':
        sex = 'Male'
    else:
        sex = 'Female'
    blinks, Total_Frames, seconds, dirs = blinkCounter(video)
    print(dirs)
    print(seconds)
    # write csv
    with open('eye_behavior_summary.csv', 'a', newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=',')
        file.writerow([video, Total_Frames, blinks, len(dirs), sex])
    with open('eye_behavior.csv', 'a', newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=',')
        file.writerow([video])
        seconds.insert(0, 'blinks')
        file.writerow(seconds)
        dirs.insert(0, 'eye-movement')
        file.writerow(dirs)

        seconds = []

# 1
# 'E013','E026','E030','E039'

# 0
#'E014','E015','E016','E018','E027'
#'E031','E033','E034','E037','E038'
#'E042','E045','E046','E048','E052'
#'E054','E060','E062'

# not working properly
# E031 E048

codesArray = ['E062']
videoCodes = create_names(codesArray, 0)
print(videoCodes)
for i in range(len(videoCodes)):
    save_blinks(videoCodes[i])
    print('finish! \n \n')
