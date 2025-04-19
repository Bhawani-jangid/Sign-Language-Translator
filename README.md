Sure! Here's a `README.md` file tailored for your Sign Language Detection project using Python, OpenCV, and MediaPipe:

---

# 🖐️ Sign Language Recognition System

This project is a **Sign Language Detection System** that uses computer vision to recognize hand gestures representing alphabets (A-Z) and space using a webcam. It employs **OpenCV**, **MediaPipe**, and **scikit-learn** with a **Random Forest Classifier** to process and classify hand landmarks.

---

## 📁 Project Structure

```
.
├── collect_imgs.py         # Collects sign images for each class using webcam
├── create_dataset.py       # Processes images with MediaPipe to extract landmarks
├── train_classifier.py     # Trains a Random Forest model using the extracted features
├── interence_classifier.py # Predicts real-time gestures and displays output
├── newinterface.py         # Advanced interface with sentence construction and hand stability checks
├── model.p                 # Trained classifier model
├── data.pickle             # Pickled dataset with features and labels
├── Sign_Language_Data/     # Collected dataset directory
└── README.md               # You’re here!
```

---

## 🔧 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy
- scikit-learn
- matplotlib
- textblob

Install dependencies using:

```bash
pip install opencv-python mediapipe scikit-learn matplotlib numpy textblob
```

---

## 🚀 How to Use

### 1. Collect Data

Run this to capture hand gesture images for A-Z and space:

```bash
python collect_imgs.py
```

Press `Q` to start capturing for each gesture. 100 images per class will be saved.

---

### 2. Create Dataset

Run this script to extract landmarks from saved images using MediaPipe:

```bash
python create_dataset.py
```

It will save `data.pickle` with features and labels.

---

### 3. Train Model

Train a Random Forest classifier using the extracted dataset:

```bash
python train_classifier.py
```

This generates the trained model and saves it to `model.p`.

---

### 4. Test Inference (Real-Time Prediction)

Test the model in real-time using your webcam:

```bash
python interence_classifier.py
```

It will draw bounding boxes and show the predicted gesture on screen.

---

### 5. Use Advanced Interface

An improved version with hand stability checks and sentence formation:

```bash
python newinterface.py
```

It waits for a stable gesture before adding it to the sentence and uses `TextBlob` for grammar correction.

---

## 🧠 Features

- Real-time hand tracking and gesture classification.
- Dataset creation and augmentation using random flips, rotations, and brightness.
- MediaPipe-based hand landmark extraction.
- Sentence construction with stability checks to avoid duplicate characters.
- Handles both single and dual-hand gestures.

---

## 📸 Sample Output

> Show predicted characters above your hand using webcam.

- Predicted label appears near the detected hand
- Sentence appears at the top of the screen with grammar correction (newinterface.py)

---

## 📦 Future Improvements

- Add support for numbers and custom gestures
- Integrate deep learning models like CNNs for higher accuracy
- Use a GUI (Tkinter / PyQt) for better interaction
- Export sentences to text or speech output

---

## 👨‍💻 Author

Developed by **[Bhawani Jangid]** 
📧 [bhawanijangid147@gmail.com]
🌐 [yourportfolio.com] 
🐙 GitHub: [@Bhawani Jangid](https://github.com/Bhawani-jangid)
Feel free to connect on GitHub or LinkedIn.

---

## 📄 License

This project is open-source and free to use for educational purposes.

---

Let me know if you want me to add a sample image, usage demo GIF, or replace `[Your Name]` with your actual name!
