import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
import os
from PIL import Image
import io
import time

# Define the test transformations
test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to match model's expected input size
    transforms.ToTensor(),           # Convert image to tensor
    transforms.Normalize((0.425, 0.415, 0.405), (0.205, 0.205, 0.205))  # Normalization for pre-trained models
])

def load_model(model_path):
    # Define the model architecture
    model = models.wide_resnet50_2(pretrained=False)  # Load architecture
    number_features = model.fc.in_features
    model.fc = nn.Linear(in_features=number_features, out_features=6)  # Adjust output classes

    # Load the state dictionary into the model
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Set the model to evaluation mode
    return model

def preprocess_frame(frame):
    # Convert the OpenCV frame (numpy array) to PIL Image and apply transforms
    pil_image = Image.open(io.BytesIO(frame))
    return test_transforms(pil_image).unsqueeze(0)  # Add batch dimension

def show_camera():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)
    
    st.html('<p class="title-home">Live Camera <a class="gradient">Prediction</a></p>')

    # Get the absolute path to the current script
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(parent_dir, "../model/model.pt")
    categories = ["Building", "Forest", "Glacier", "Mountain", "Sea", "Street"]

    # Load the model
    if not os.path.exists(model_path):
        st.error(f"Model file not found at: {model_path}")
        return
    model = load_model(model_path)

    # Streamlit camera input
    image = st.camera_input("Capture Image")
    # If the user has uploaded an image
    if image is not None:
        # Convert the uploaded file to bytes and then process it
        image_bytes = image.getvalue()
        
        # Preprocess the image
        input_tensor = preprocess_frame(image_bytes)

        # Get predictions
        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs, 1)
            prediction = categories[predicted.item()]

        # Display the image and prediction
        st.image(image, caption="Captured Image", use_column_width=True)
        st.success(f"**Prediction**: {prediction}")
