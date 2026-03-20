# handkamera.py
import cv2
import mediapipe as mp

# Initiera MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

# === FUNKTIONER FÖR GESTER ===
def is_thumb_up(lm):
    return lm[4][1] < lm[0][1]      # tumme högre än handleden

def is_thumb_down(lm):
    return lm[4][1] > lm[0][1]# tumme lägre än handleden
# --- Funktioner för 15 handpositioner ---
def finger_state(lm):
    """Returnerar [thumb, index, middle, ring, pinky] med 1=uppe, 0=nere"""
    thumb  = 1 if lm[4][1] < lm[3][1] else 0
    index  = 1 if lm[8][1] < lm[6][1] else 0
    middle = 1 if lm[12][1] < lm[10][1] else 0
    ring   = 1 if lm[16][1] < lm[14][1] else 0
    pinky  = 1 if lm[20][1] < lm[18][1] else 0
    return [thumb, index, middle, ring, pinky]

# 15 positioner
def pos_1(f):  return f == [1,0,0,0,0]
def pos_2(f):  return f == [0,1,0,0,0]
def pos_3(f):  return f == [0,0,1,0,0]
def pos_4(f):  return f == [0,0,0,1,0]
def pos_5(f):  return f == [0,0,0,0,1]
def pos_6(f):  return f == [1,1,0,0,0]
def pos_7(f):  return f == [1,0,1,0,0]
def pos_8(f):  return f == [1,0,0,1,0]
def pos_9(f):  return f == [1,0,0,0,1]
def pos_10(f): return f == [0,1,1,0,0]
def pos_11(f): return f == [0,1,0,1,0]
def pos_12(f): return f == [0,1,0,0,1]
def pos_13(f): return f == [0,0,1,1,0]
def pos_14(f): return f == [0,0,1,0,1]
def pos_15(f): return f == [0,0,0,1,1]




# Starta kameran
cap = cv2.VideoCapture(0)
print("Tryck Q för att avsluta")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # --- HANTERA HANDDATA ---
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            # Rita hand på skärmen
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Hämta punktdata (landmarks)
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # === KOLLA GESTER ===
            if is_thumb_up(lm_list):
                cv2.putText(frame, "TUMME UPP", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)

            elif is_thumb_down(lm_list):
                cv2.putText(frame, "TUMME NER", (30, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
            
            
            # Kontrollera alla 15 positioner
            f = finger_state(lm_list)

            if   pos_1(f):  msg="Pos 1: Tumme"
            elif pos_2(f):  msg="Pos 2: Pekfinger"
            elif pos_3(f):  msg="Pos 3: Långfinger"
            elif pos_4(f):  msg="Pos 4: Ringfinger"
            elif pos_5(f):  msg="Pos 5: Lillfinger"
            elif pos_6(f):  msg="Pos 6: Tumme+Pek"
            elif pos_7(f):  msg="Pos 7: Tumme+Lång"
            elif pos_8(f):  msg="Pos 8: Tumme+Ring"
            elif pos_9(f):  msg="Pos 9: Tumme+Lillfinger"
            elif pos_10(f): msg="Pos 10: Pek+Lång (Peace)"
            elif pos_11(f): msg="Pos 11: Pek+Ring"
            elif pos_12(f): msg="Pos 12: Pek+Lillfinger"
            elif pos_13(f): msg="Pos 13: Lång+Ring"
            elif pos_14(f): msg="Pos 14: Lång+Lillfinger"
            elif pos_15(f): msg="Pos 15: Ring+Lillfinger"
            else: msg="Ingen position"

            cv2.putText(frame, msg, (30,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)



    cv2.imshow("MediaPipe Hands", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
