import cv2
import os
import numpy as np
import random
import string  # Import string module for A-Z

# Constants
DATA_DIR = "Sign_Language_Data"  # Directory to store images
classes = list(string.ascii_uppercase) + ["space"]# A-Z classes
dataset_size = 100  # Number of images per class

# Create dataset folders
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

cap = cv2.VideoCapture(0)

for class_label in classes:
    class_dir = os.path.join(DATA_DIR, class_label)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for sign "{class_label}"... Press "Q" to start.')

    # Wait until user presses 'Q' to start collection
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, f'Collecting "{class_label}" - Press "Q"!', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            continue
        
        # ✅ Apply random transformations for more variations
        if random.random() > 0.5:
            frame = cv2.flip(frame, 1)  # Flip horizontally
        
        angle = random.randint(-15, 15)  # Random rotation angle
        h, w = frame.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        frame = cv2.warpAffine(frame, M, (w, h))

        brightness = random.uniform(0.7, 1.3)  # Adjust brightness
        frame = np.clip(frame * brightness, 0, 255).astype(np.uint8)

        # ✅ Save images with clear labeling (class_label + index)
        img_path = os.path.join(class_dir, f"{class_label}_{counter}.jpg")
        cv2.imwrite(img_path, frame)

        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        
        counter += 1

cap.release()
cv2.destroyAllWindows()

