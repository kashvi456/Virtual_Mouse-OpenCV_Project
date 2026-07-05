import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math

# 1. Model Initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

#2. Display Configuration
screen_w, screen_h = pyautogui.size()
cam_w, cam_h = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

#3. Smoothing Variables
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
smooth_factor = 5

frame_margin = 100

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x*cam_w), int(lm.y*cam_h)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                x_index, y_index = lm_list[8][1:]
                x_mid, y_mid = lm_list[12][1:]
                x_thumb, y_thumb = lm_list[4][1:]

                fingers = []
                fingers.append(1 if lm_list[4][1] < lm_list[3][1] else 0)
                for id in range(8, 21, 4):
                    fingers.append(1 if lm_list[id][2] < lm_list[id-2][2] else 0)
                
                # Draw the active boundinng box ont he camera feed
                cv2.rectangle(img, (frame_margin, frame_margin), (cam_w - frame_margin, cam_h - frame_margin), (255, 0, 255), 2)

                # ------Gesture 1:Move cursor (Index finger up) ------
                if fingers[1] == 1 and fingers[2] == 0:
                    screen_x = np.interp(x_index, (frame_margin, cam_w - frame_margin), (0, screen_w))
                    screen_y = np.interp(y_index, (frame_margin, cam_h - frame_margin), (0, screen_h))

                    curr_x = prev_x + (screen_x - prev_x) / smooth_factor
                    curr_y = prev_y + (screen_y - prev_y) / smooth_factor

                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

                # ------Gesture 2: Click (Distance between Index and Thumb is small) ------
                if fingers[1] == 1:
                    distance = math.hypot(x_index - x_thumb, y_index - y_thumb)
                    if distance < 40:
                        cv2.circle(img, (x_index, y_index), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                        pyautogui.sleep(0.2)
                
                # ------ Gesture 3: Scroll(Index and Middle fingers up) ------
                if fingers[1] == 1 and fingers[2] == 1:
                    distance = math.hypot(x_index - x_mid, y_index - y_mid)
                    if distance < 50:
                        pyautogui.scroll(-30)
                
    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
