import cv2
import mediapipe as mp
import pyautogui
import subprocess
import time
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

def get_finger_states(landmarks):
    states = []
    for i, tip_id in enumerate(finger_tips):
        tip = landmarks.landmark[tip_id]
        base = landmarks.landmark[tip_id - 2]
        if i == 0:  # thumb
            states.append(tip.x < base.x)
        else:
            states.append(tip.y < base.y)
    return states

def gesture_action(states, last_time):
    now = time.time()
    if now - last_time < 2.0:  
        return last_time
    
    # 2
    if states == [False, True, False, False, False]:
        print(" Launching Inventor")
        subprocess.Popen(["route to Inventor.exe"])
        time.sleep(3)
        return now

    # 4
    if states == [False, False, True, False, False]:
        print("Flip-off detected. Shutting down!")
        time.sleep(3)
        subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)
        return now
    
    # 6
    if states == [False, True, True, False, False]:
        print(" Launching VsCode")
        subprocess.Popen(["route to Code.exe"])
        time.sleep(3)
        return now
    
    # 8
    if states == [False, False, False, True, False]:
        print(" Launching brightspace")
        subprocess.Popen(["start", "https://brightspace.com"], shell=True)
        time.sleep(3)
        return now
    
    # 10
    if states == [False, True, False, True, False]:
        print(" Launching Calendar")
        subprocess.Popen(["start", "https://calendar.google.com/calendar/u/0/r?pli=1"], shell=True)
        time.sleep(3)
        return now
    
    # 12
    if states == [False, False, True, True, False]:
        print(" Launching Chat")
        subprocess.Popen(["start", "https://chatgpt.com"], shell=True)
        time.sleep(3)
        return now
    
    # 14
    if states == [False, True, True, True, False]:
        print(" Launching KiCad")
        subprocess.Popen(["route to kicad.exe"])
        time.sleep(3)
        return now

    # 16
    if states == [False, False, False, False, True]:
        print(" Launching Firefox")
        subprocess.Popen(["route to firefox.exe"])
        time.sleep(3)
        return now
    
    #  18
    if states == [False, True, False, False, True]:
        print(" Launching Outlook")
        subprocess.Popen(["route to OUTLOOK.EXE"])
        time.sleep(3)
        return now
    
    # 20
    if states == [False, False, True, False, True]:
        print("Launching Arduino")
        subprocess.Popen(["route to Arduino IDE.exe"])
        time.sleep(3)
        return now
    
    # 22 finger
    if states == [False, True, True, False, True]:
        print("Launching Steam")
        subprocess.Popen(["route to Steam.exe"])
        time.sleep(3)
        return now

    # 28
    if states == [False, True, True, True, True]:
        print(" Launching Desmos")
        subprocess.Popen(["start", "https://www.desmos.com/scientific"], shell=True)
        time.sleep(3)
        return now

    # 30
    if states == [False, True, True, True, True]:
        print(" Launching YT")
        subprocess.Popen(["start", "https://www.youtube.com"], shell=True)
        time.sleep(3)
        return now
    return last_time

last_action_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

            states = get_finger_states(lm)
            last_action_time = gesture_action(states, last_action_time)

    cv2.imshow("Gesture Watcher", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
