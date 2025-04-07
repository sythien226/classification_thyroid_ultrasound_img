# 🧠 Thyroid Ultrasound Image Classification

This project focuses on classifying thyroid ultrasound images into two categories: **Benign** and **Malignant** using deep learning models. It includes a web-based interface built with Flask, allowing users to upload and classify ultrasound images easily.

---

## 📁 Project Structure


---

## 🚀 Features

- ✅ Upload thyroid ultrasound images through a web interface  
- ✅ Predict whether an image is **Benign** or **Malignant**  
- ✅ Built with Flask (lightweight and easy to deploy)  
- ✅ Supports custom model replacement  
- ✅ Augmentation & preprocessing included in pipeline  

---

## 🧠 Model Information

- **Framework**: TensorFlow / Keras (or PyTorch via `timm`)
- **Input size**: 224x224
- **Classification**: Binary (Benign vs. Malignant)
- **Augmentation**: Rotation, Zoom, Flip, Shift, etc.
- **Performance**: High accuracy on the custom dataset

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sythien226/classification_thyroid_ultrasound_img.git
cd classification_thyroid_ultrasound_img


###2.Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

###3.Run app
python app.py

