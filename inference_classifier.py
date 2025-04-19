import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    # Convert image to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for hand landmarks
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        # Extract landmarks for each hand
        for hand_landmarks in results.multi_hand_landmarks:
            x_.clear()
            y_.clear()
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            # Normalize and append the features for each hand
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # If only one hand is detected, duplicate the features for the second hand (use same features)
        if len(results.multi_hand_landmarks) == 1:
            # Duplicate the features from the first hand to make up 84 features
            data_aux.extend(data_aux)  # Copy the data from the first hand for the second hand

        # Ensure that the data has exactly 84 features
        if len(data_aux) != 84:
            print(f"Error: Expected 84 features, but got {len(data_aux)}")
            data_aux = [0] * 84  # Reset to 84 zeros if feature count is incorrect

        # Prepare the input for prediction
        prediction = model.predict([np.asarray(data_aux)])

        # Get the predicted label
        predicted_character = prediction[0]

        # Draw a rectangle around the detected hand
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

    # Display the frame with the prediction
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

# Release resources
cap.release()
cv2.destroyAllWindows()
