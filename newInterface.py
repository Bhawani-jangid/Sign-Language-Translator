import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
from textblob import TextBlob

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles  # Ensure correct drawing styles
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

sentence = ""  # Stores the predicted sentence
prev_char = None  
capture_delay = 1.5  # Delay between captures to prevent duplicate characters
stable_threshold = 0.01  # Defines how stable the hand must be

hand_positions = []  # Stores previous hand positions for stability check

def is_hand_stable(hand_positions, threshold=stable_threshold):
    """Check if the hand remains stable based on movement threshold"""
    if len(hand_positions) < 5:  # Need at least 5 frames
        return False

    x_positions = [pos[0] for pos in hand_positions]
    y_positions = [pos[1] for pos in hand_positions]

    # Calculate movement range
    x_range = max(x_positions) - min(x_positions)
    y_range = max(y_positions) - min(y_positions)

    return x_range < threshold and y_range < threshold  # Return True if stable

while True:
    data_aux = []
    x_, y_ = [], []

    ret, frame = cap.read()
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks on the image
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

        # Extract landmarks for each hand
        for hand_landmarks in results.multi_hand_landmarks:
            x_.clear()
            y_.clear()
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            # Store the current hand position for stability check
            hand_positions.append((np.mean(x_), np.mean(y_)))

            if len(hand_positions) > 10:  # Keep last 10 positions
                hand_positions.pop(0)

            # Process only if hand is stable
            if is_hand_stable(hand_positions):
                # Normalize and append the features for each hand
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

        # If only one hand is detected, duplicate the features for the second hand
        if len(results.multi_hand_landmarks) == 1:
            data_aux.extend(data_aux)  # Copy the data from the first hand for the second hand

        # Ensure the data has exactly 84 features
        if len(data_aux) != 84:
            print(f"Error: Expected 84 features, but got {len(data_aux)}")
            data_aux = [0] * 84  # Reset to 84 zeros if feature count is incorrect

        # Predict the letter
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = prediction[0]

        # Avoid repeating the same character
        if predicted_character != prev_char:
            sentence += predicted_character
            prev_char = predicted_character
            time.sleep(capture_delay)  # Delay before next letter capture

    # Apply spell correction
    corrected_sentence = str(TextBlob(sentence).correct())

    # Display Results
    cv2.putText(frame, "Sentence: " + corrected_sentence, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press 'Space' for space | 'Backspace' to delete | 'Enter' to clear", (20, H - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)

    if key == 8:  # Backspace
        sentence = sentence[:-1]
    elif key == 32:  # Space
        sentence += " "
    elif key == 13:  # Enter
        sentence = ""
    elif key == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
