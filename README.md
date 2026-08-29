# 🎨 RGB Color Detection

A simple **Streamlit + OpenCV** application that detects the dominant color of an image by analyzing its RGB values.

## ✨ Features

- 📷 Capture an image using camera
- 📁 Upload an image
- 🎨 Detect dominant RGB color
- 📊 Display Red, Green, and Blue values
- 📹 Local webcam support

## 🛠️ Technologies

- Python
- Streamlit
- OpenCV
- NumPy

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
streamlit run app.py
```

### 3. Open in browser

```text
http://localhost:8501
```

## 📂 Project Structure

```text
rgb_detection/
├── app.py
├── requirements.txt
└── README.md
```

## 🎯 How It Works

The application calculates the average **Red, Green, and Blue** values of the image and identifies the channel with the highest value as the dominant color.