import cv2
import numpy as np
import mediapipe as mp


def calc_angle(a,b,c):
    #x and y coordinates of each point (should, elbow, wrist)
    a = np.array([a.x,a.y])
    b = np.array([b.x,b.y])
    c = np.array([c.x,c.y])
    #pointing the vector from point a to b and then point b to c
    ab = b - a
    bc = c - b

    dot_product = np.dot(ab,bc)

    angle_calculation = np.arccos(dot_product/(np.linalg.norm(ab)*np.linalg.norm(bc)))
    #Converting to degrees
    return np.degrees(angle_calculation)



def main():
    pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    vid = cv2.VideoCapture(0)
    count = 0
    state = 'up'

    while True:
        ret,frame = vid.read()
        if ret:
            frame,count,state = process_frame(frame,pose,count,state)

            cv2.putText(frame,"Press 'R' to reset count",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(frame,"Press 'Q' to exit",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.imshow('Camera',frame)


        if cv2.waitKey(1) & 0xFF == ord('r'):
            count = 0 #reset the count

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()



def process_frame(frame,pose_detector,count,state):
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = pose_detector.process(rgb_frame)

    some_threshold = 160
    some_other_threshold = 30



    if results.pose_landmarks:


        mp.solutions.drawing_utils.draw_landmarks(frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)

        left_shoulder = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST]

        right_shoulder = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]

        left_angle = calc_angle(left_shoulder,left_elbow,left_wrist)
        right_angle = calc_angle(right_shoulder,right_elbow,right_wrist)

        angle = max(left_angle,right_angle)


        #to debug: use the print below
        #print(f"Angle: {angle}, State: {state}, Count: {count}")

        if angle > some_threshold and state == 'up':
            state = 'down'
        elif angle < some_other_threshold and state == 'down':
            count += 1
            state = 'up'

        x,y = 50,50
        #cv2.putText(frame,f"Angle: {angle}",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        cv2.putText(frame,f"Count: {count}",(x,y+60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


    return frame,count,state


main()