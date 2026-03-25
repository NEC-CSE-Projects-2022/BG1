
# BG1 –  Comparative Analysis of Quantum and Multi-Model Deep Learning Approaches for Skin Lesion Classification

## Team Info
- 22471A0583 — **CHINNAPAREDDY ANJALI REDDY** ( [LinkedIn](https://www.linkedin.com/in/anjali-reddy-chinnapareddy-434598385) )
_Work Done: Data preprocessing, model training, result analysis_

- 22471A0587 — **DOGIPARTHI DHANUSHA** ( [LinkedIn](https://www.linkedin.com/in/dogiparthi-dhanusha-a7a812276/) )
_Work Done: Dataset collection, EDA, augmentation_

- 22471A0581 — **SHAIK CHIKLI ASIFA** ( [LinkedIn](https://www.linkedin.com/in/shaik-chikli-asifa-176a61355/) )
_Work Done: Deep learning model implementation_



---

## Abstract
Skin lesion classification plays a crucial role in early detection of skin cancer and other dermatological diseases. This project presents a comparative study between Quantum Machine Learning models and traditional Deep Learning models for classifying dermoscopic skin lesion images.

Quantum Neural Network (QNN) and Quantum Support Vector Classifier (QSVC) were implemented and compared with deep learning architectures such as EfficientNetB0, MobileNetV3, ResNet18, and EFAM-Net. Experimental results show that classical deep learning models outperform quantum-based approaches due to better feature extraction and training stability.

EfficientNetB0 achieved the highest accuracy of 90.21%, demonstrating the effectiveness of convolutional neural networks in medical image classification.

---

## Paper Reference (Inspiration)
👉 **[Paper Title Comparative Analysis of Quantum and Multi-Model Deep Learning Approaches for Skin Lesion Classification
  – Author Names Moturi Sireesha, Anjali Reddy, Dhanusha, Asifa, Chandra Mouli, Sasidhar
 ](https://ieeexplore.ieee.org/document/10613907)**


---

## Our Improvement Over Existing Paper
Implemented multiple deep learning architectures under identical conditions for fair comparison
Improved preprocessing pipeline using augmentation techniques
Applied transfer learning to enhance model accuracy
Compared quantum models with deep learning models to analyze real-world performance
Achieved improved accuracy using EfficientNetB0 and MobileNetV3

---

## About the Project
This project classifies skin disease images into different categories using deep learning and quantum machine learning models.

Workflow

Input Image → Preprocessing → Feature Extraction → Model Training → Prediction Output

Why this project is useful
-Helps in early detection of skin cancer
-Reduces dependency on manual diagnosis
-Supports doctors in medical decision-making
-Improves diagnostic accuracy using AI

---

## Dataset Used
👉 **[HAM10000 Dataset (Human Against Machine with 10000 images)](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)**

**Dataset Details:**
-Contains dermoscopic images of skin lesions
-Includes both benign and malignant classes
-Dataset is imbalanced, requiring augmentation
-Images captured under different lighting conditions
-Used widely as benchmark dataset for skin cancer classification

---

## Dependencies Used
-Python
-TensorFlow / PyTorch
-NumPy
-Pandas
-Matplotlib
-Scikit-learn
-OpenCV
-Qiskit (for quantum models)

---

## EDA & Preprocessing
-Checked class distribution of dataset
-Applied data augmentation techniques:
-Rotation
-Horizontal flipping
-Resizing images
-Converted images into tensors
-Normalized pixel values
-Applied stratified data splitting into:
-Training set
-Validation set
-Testing set
---

## Model Training Info
Deep learning models used:

-EfficientNetB0
-MobileNetV3
-ResNet18
-EfficientFormer
-EFAM-Net

Quantum models used:

-Quantum Neural Network (QNN)
-Quantum Support Vector Classifier (QSVC)

Training configuration:

-Optimizer: Adam
-Learning rate: 0.0001
-Batch size: 32
-Epochs: 30
-Loss function: Categorical Cross Entropy
-Transfer learning used for better performance

---

## Model Testing / Evaluation
Evaluation metrics used:

Accuracy
Precision
Recall
F1-score

Models were evaluated on unseen test dataset to ensure fairness and reliability.

---

## Results
Model	Accuracy
. Accuracy: 94.00%
. Precision: 64.00%
. Recall: 57.00%
. F1-score: 67.00%

---

## Limitations & Future Work
Limitations:

-Dataset imbalance affects performance
-Quantum models limited by simulator constraints
-Requires high computational resources

Future Work:

-Hybrid quantum-classical models
-More balanced datasets
-Improved feature encoding techniques
-Real-time medical deployment

---

## Deployment Info
The trained model can be deployed using:

-Streamlit web app
-Flask API
-Cloud platforms (AWS, GCP)
-Integration with hospital diagnostic systems

Users can upload skin images and get prediction results instantly.

---
