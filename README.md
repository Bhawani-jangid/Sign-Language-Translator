# Sign Language Recognition Using Hand Gestures

This project uses OpenCV, Mediapipe, and Machine Learning to recognize American Sign Language (A-Z + space).

## 🧠 Features
- Collect sign language images via webcam
- Create landmark dataset using MediaPipe
- Train RandomForest classifier
- Real-time prediction and sentence generation
- Sentence correction using TextBlob

## 📂 Files
- `collect_imgs.py`: Collect images A-Z using webcam
- `create_dataset.py`: Generate landmark data
- `train_classifier.py`: Train model
- `inference_classifier.py`: Basic real-time prediction
- `newinterface.py`: Advanced interface with sentence creation

## 🛠 Requirements
Install dependencies:

```bash
pip install -r requirements.txt
