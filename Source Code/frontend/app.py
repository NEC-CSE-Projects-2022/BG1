from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import json, os, uuid, math
import numpy as np
from datetime import datetime

# ===============================
# APP SETUP
# ===============================
app = Flask(__name__, 
            template_folder="templates",
            static_folder="static")

CORS(app)

DEVICE = torch.device("cpu")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===============================
# PAGE ROUTES
# ===============================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dataset")
def dataset():
    return render_template("dataset.html")

@app.route("/skinpredict")
def skinpredict():
    return render_template("skinpredict.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


# ===============================
# STORAGE
# ===============================
PRED_DIR = os.path.join(BASE_DIR, "predictions")
IMG_DIR = os.path.join(PRED_DIR, "images")
META_FILE = os.path.join(PRED_DIR, "metadata.json")

os.makedirs(IMG_DIR, exist_ok=True)

if not os.path.exists(META_FILE):
    with open(META_FILE, "w") as f:
        json.dump([], f)

# ===============================
# JSON HELPERS
# ===============================
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ===============================
# LOAD CLASSES
# ===============================
CLASS_NAMES = load_json(os.path.join(BASE_DIR, "class_indices.json"), [])
CLASS_DESCRIPTIONS = load_json(os.path.join(BASE_DIR, "class_descriptions.json"), {})

if not CLASS_NAMES:
    raise Exception("class_indices.json missing or empty.")

NUM_CLASSES = len(CLASS_NAMES)

# ===============================
# TRANSFORM
# ===============================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ===============================
# SKIN CHECK
# ===============================
def skin_ratio(image):
    img = np.array(image)
    if img.ndim != 3:
        return 0.0

    R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]

    skin = (
        (R > 80) &
        (G > 30) &
        (B > 15) &
        (R > G) &
        (R > B) &
        (np.abs(R - G) > 10)
    )

    return float(np.mean(skin))

# ===============================
# ENTROPY
# ===============================
def entropy(probs):
    return -sum(p * math.log(p + 1e-9) for p in probs)

# ===============================
# MODEL LOADER
# ===============================
def load_model(model_name, weight_path):

    if not os.path.exists(weight_path):
        print(f"⚠ Missing: {weight_path}")
        return None

    if model_name == "resnet":
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)

    elif model_name == "efficientnet":
        model = models.efficientnet_b0(weights=None)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)

    elif model_name == "mobilenet":
        model = models.mobilenet_v3_large(weights=None)
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, NUM_CLASSES)

    elif model_name == "efamnet":
        model = models.efficientnet_b0(weights=None)
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)

    else:
        return None

    model.load_state_dict(torch.load(weight_path, map_location=DEVICE))
    model.eval()
    return model


# ===============================
# LOAD MODELS
# ===============================
cnn_models = {}

model_paths = {
    "resnet": os.path.join(BASE_DIR, "models/resnet18_skin.pth"),
    "efficientnet": os.path.join(BASE_DIR, "models/best_efficientnet_b0.pth"),
    "mobilenet": os.path.join(BASE_DIR, "models/mobilenetv3_skin.pth"),
    "efamnet": os.path.join(BASE_DIR, "models/efamnet_skin.pth")
}

for name, path in model_paths.items():
    model = load_model(name, path)
    if model:
        cnn_models[name] = model

if not cnn_models:
    raise Exception("No models loaded.")

# ===============================
# PREDICT ROUTE
# ===============================
@app.route("/predict", methods=["POST"])
def predict():

    files = request.files.getlist("images")
    if not files:
        return jsonify({"error": "No images uploaded"}), 400

    results = []
    metadata = load_json(META_FILE, [])

    for idx, file in enumerate(files):

        try:
            image = Image.open(file).convert("RGB")

            # Skin gate
            if skin_ratio(image) < 0.15:
                results.append({
                    "index": idx,
                    "filename": file.filename,
                    "rejected": True,
                    "reason": "Not a skin lesion image"
                })
                continue

            tensor = transform(image).unsqueeze(0)

            probs_all = []
            cnn_results = {}

            with torch.no_grad():
                for name, model in cnn_models.items():
                    probs = torch.softmax(model(tensor), dim=1)[0].numpy()
                    probs_all.append(probs)

                    top_idx = int(np.argmax(probs))
                    class_name = CLASS_NAMES[top_idx]

                    cnn_results[name] = {
                        "class_code": class_name,
                        "confidence": round(float(probs[top_idx]) * 100, 2),
                        "description": CLASS_DESCRIPTIONS.get(class_name, "")
                    }

            avg_probs = np.mean(probs_all, axis=0)

            if max(avg_probs) < 0.45 and entropy(avg_probs) > 1.8:
                results.append({
                    "index": idx,
                    "filename": file.filename,
                    "rejected": True,
                    "reason": "Low confidence"
                })
                continue

            uid = str(uuid.uuid4())
            image.save(os.path.join(IMG_DIR, f"{uid}.jpg"))

            metadata.append({
                "id": uid,
                "filename": file.filename,
                "timestamp": datetime.now().isoformat(),
                "cnn_results": cnn_results
            })

            results.append({
                "index": idx,
                "filename": file.filename,
                "cnn_results": cnn_results
            })

        except Exception as e:
            results.append({
                "index": idx,
                "filename": file.filename,
                "rejected": True,
                "reason": str(e)
            })

    save_json(META_FILE, metadata)
    return jsonify({"results": results})


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
