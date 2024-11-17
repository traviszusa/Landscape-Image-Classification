import os
import zipfile
import shutil
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import streamlit as st

# Helper function to load the model
def load_model():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(parent_dir, "../model/model.pt")
    
    model = models.wide_resnet50_2(pretrained=False)  # Load architecture
    num_features = model.fc.in_features
    model.fc = nn.Linear(in_features=num_features, out_features=6)  # Adjust output layer for 6 categories
    
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model

# Prediction function
def predict_image(model, image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.425, 0.415, 0.405), (0.205, 0.205, 0.205))
    ])
    image = transform(image).unsqueeze(0)  # Add batch dimension
    outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    return predicted.item()

# Process batch ZIP
def process_batch_zip(uploaded_zip, model, output_dir, zip_name):
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        zip_ref.extractall(output_dir)  # Extract all files to the output directory

    # Create directories for categories
    categories = ["Building", "Forest", "Glacier", "Mountain", "Sea", "Street"]
    for category in categories:
        os.makedirs(os.path.join(output_dir, category), exist_ok=True)

    # Process each image in the extracted folder
    for img_file in Path(output_dir).rglob("*.*"):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            image = Image.open(img_file)
            predicted_class = predict_image(model, image)

            # Rename and save the image in the corresponding category folder
            new_name = f"{categories[predicted_class]}_{img_file.name}"
            new_path = os.path.join(output_dir, categories[predicted_class], new_name)
            image.save(new_path)

    # Create a ZIP file with classified images
    result_zip_path = os.path.join(output_dir, f"{zip_name}.zip")
    shutil.make_archive(result_zip_path.replace(".zip", ""), 'zip', output_dir)

    return result_zip_path

# Main function for the upload page
def show_upload():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)
    
    st.html('<p class="title-home">Upload <a class="gradient">Image</a></p>')

    # Load the model
    model = load_model()

    # Allow user to select the processing mode
    option = st.selectbox("Select processing mode:", ["Single Image", "Batch (ZIP)"])

    if option == "Single Image":
        # Single image upload
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Perform prediction
            predicted_class = predict_image(model, image)
            categories = ["Building", "Forest", "Glacier", "Mountain", "Sea", "Street"]
            st.write(f"Predicted Category: **{categories[predicted_class]}**")

    elif option == "Batch (ZIP)":
        # Custom ZIP file name input
        zip_name = st.text_input("Enter the desired name for the output ZIP file (without extension):", "classified_images")

        # Batch image upload via ZIP file
        uploaded_zip = st.file_uploader("Upload a ZIP file with images...", type=["zip"])
        if uploaded_zip is not None:
            # Output directory for extracted images
            output_dir = os.path.join("temp", "extracted_images")
            os.makedirs(output_dir, exist_ok=True)

            # Process the ZIP file and get the result ZIP file
            result_zip = process_batch_zip(uploaded_zip, model, output_dir, zip_name)

            # Offer the result ZIP file for download
            with open(result_zip, "rb") as f:
                st.download_button(
                    label="Download Classified Images ZIP",
                    data=f,
                    file_name=f"{zip_name}.zip",
                    mime="application/zip"
                )