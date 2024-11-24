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

def display_weather_columns():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Cerah</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Wide-Angle Lens (10-24mm) atau Tilt-Shift Lens</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 100 - 200</li>
                                <li><strong>Aperture</strong>: f/8 - f/11</li>
                                <li><strong>Shutter Speed</strong>: 1/125 detik</li>
                            </ul>
                        </div>
                    </div>
                ''')
    with col2:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Berawan</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Wide-Angle Lens atau Standard Zoom (24-70mm)</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 200 - 400</li>
                                <li><strong>Aperture</strong>: f/5.6 - f/8</li>
                                <li><strong>Shutter Speed</strong>: 1/60 - 1/125 detik</li>
                            </ul>
                        </div>
                    </div>
                ''')
    with col3:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Hujan</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Wide-angle atau telephoto (70-200mm)</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 400 - 800</li>
                                <li><strong>Aperture</strong>: f/4 - f/8</li>
                                <li><strong>Shutter Speed</strong>: 1/125 - 1/250 detik</li>
                            </ul>
                        </div>
                    </div>
                ''')
    col4, col5, col6 = st.columns(3)
    with col4:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Golden Hour</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Wide-angle atau lensa prime (35mm atau 50mm)</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 100 - 200</li>
                                <li><strong>Aperture</strong>: f/5.6 - f/8</li>
                                <li><strong>Shutter Speed</strong>: 1/60 - 1/125 detik</li>
                            </ul>
                        </div>
                    </div>
                ''')
    with col5:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Malam</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Lensa wide dengan aperture besar (f/1.8 atau f/2.8)</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 800 - 3200</li>
                                <li><strong>Aperture</strong>: f/2.8 - f/5.6</li>
                                <li><strong>Shutter Speed</strong>: 1 - 30 detik</li>
                            </ul>
                        </div>
                    </div>
                ''')
    with col6:
        st.html('''<div class="container">
                        <div class="container-content">
                            <h3 style="text-align: center;">Salju</h3>
                            <p class="zero-margin text-justify"><strong>Lensa</strong>: Wide-Angle Lens atau Standard Lens dengan Weather-Sealing</p>
                            <p class="zero-margin"><strong>Setting Kamera</strong></p>
                            <ul class="ul-content">
                                <li><strong>ISO</strong>: 200 - 400</li>
                                <li><strong>Aperture</strong>: f/8 - f/11</li>
                                <li><strong>Shutter Speed</strong>: 1/125 atau lebih cepat</li>
                            </ul>
                        </div>
                    </div>
                ''')

def show_camera():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)
    
    st.html('<p class="title-home">Live Camera <span class="gradient">Prediction</span></p>')

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

        if prediction == "Building":
            st.expander(f"Predicted Category: {prediction}").write('''
                Building merupakan kategori yang menunjukkan bahwa objek tersebut merupakan bangunan maupun gedung, sehingga dapat diidentifikasi sebagai objek bangunan.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Golden Hour</strong>: Cahaya lembut saat matahari terbit atau terbenam akan memberikan bangunan tampilan yang hangat dan dramatis. Bayangan panjang akan menambah dimensi pada arsitektur.</li>
                                    <li><strong>Cerah</strong>: Cuaca cerah memungkinkan Anda mendapatkan detail yang tajam pada bangunan dan langit biru yang cerah akan memberikan kontras yang menarik.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Bangunan").html('''
                <ul class="ul-content">
                    <li>Gunakan lensa tilt-shift untuk mengoreksi perspektif vertikal</li>
                    <li>Manfaatkan simetri dan pola dalam arsitektur</li>
                    <li>Coba sudut ekstrem (sangat rendah atau tinggi) untuk komposisi unik</li>
                    <li>Foto di blue hour untuk pencahayaan seimbang eksterior dan interior</li>
                    <li>Perhatikan detail arsitektur dan tekstur untuk foto close-up</li>
                </ul>
            ''')
        elif prediction == "Forest":
            st.expander(f"Predicted Category: {prediction}").write('''
                Forest merupakan kategori yang menunjukkan bahwa objek tersebut adalah hutan atau area hijau alami yang terdiri dari pepohonan, semak, dan ekosistem yang mendukung kehidupan flora dan fauna. Kategori ini mengindikasikan bahwa lingkungan yang terdeteksi termasuk dalam wilayah hutan.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Golden Hour</strong>: Sinar matahari menembus pepohonan menciptakan efek dramatis dan hangat. Cahaya lembut akan menonjolkan tekstur kulit pohon dan dedaunan.</li>
                                    <li><strong>Hujan</strong>: Hutan setelah hujan terlihat segar dan hijau. Tetesan air pada daun akan berkilau dan menciptakan suasana yang tenang.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Hutan").html('''
                <ul class="ul-content">
                    <li>Cari komposisi dengan framing alami menggunakan pepohonan</li>
                    <li>Manfaatkan sinar matahari yang menembus dedaunan untuk efek dramatik</li>
                    <li>Gunakan tripod untuk foto detail dalam kondisi cahaya rendah</li>
                    <li>Tangkap tekstur dan pola alami dari batang pohon dan dedaunan</li>
                    <li>Eksperimen dengan depth of field untuk menciptakan lapisan visual</li>
                </ul>
            ''')
        elif prediction == "Glacier":
            st.expander(f"Predicted Category: {prediction}").write('''
                Glacier merupakan kategori yang menunjukkan bahwa objek tersebut adalah gletser atau lapisan es yang luas, yang biasanya terdapat di daerah pegunungan tinggi atau kutub. Gletser ini mencair dan membentuk aliran air yang mengalir ke laut.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Cerah</strong>: Cuaca cerah akan menonjolkan warna biru es yang menakjubkan dan memberikan kontras yang kuat dengan langit biru.</li>
                                    <li><strong>Berawan</strong>: Cahaya yang tersebar pada hari berawan akan mengurangi kontras yang terlalu tinggi dan membantu Anda mendapatkan detail yang lebih halus pada permukaan es.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Gletser").html('''
                <ul class="ul-content">
                    <li>Cari komposisi dengan framing alami menggunakan pepohonan</li>
                    <li>Manfaatkan sinar matahari yang menembus dedaunan untuk efek dramatik</li>
                    <li>Gunakan tripod untuk foto detail dalam kondisi cahaya rendah</li>
                    <li>Tangkap tekstur dan pola alami dari batang pohon dan dedaunan</li>
                    <li>Eksperimen dengan depth of field untuk menciptakan lapisan visual</li>
                </ul>
            ''')
        elif prediction == "Mountain":
            st.expander(f"Predicted Category: {prediction}").write('''
                Mountain merupakan kategori yang menunjukkan bahwa objek tersebut adalah gunung, biasanya berupa struktur geologis yang lebih tinggi dari sekitarnya. Gunung dapat berupa puncak tajam atau lebih landai dan ditemukan di seluruh dunia.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Golden Hour</strong>: Cahaya lembut akan memberikan gunung tampilan yang dramatis, terutama saat matahari terbit atau terbenam di balik puncak gunung.</li>
                                    <li><strong>Malam</strong>: Jika Anda ingin menangkap keindahan bintang atau jalur susu, malam adalah waktu yang tepat untuk memotret gunung.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Gunung").html('''
                <ul class="ul-content">
                    <li>Gunakan filter gradasi untuk menyeimbangkan langit dan foreground</li>
                    <li>Cari elemen foreground menarik untuk depth</li>
                    <li>Waktu terbaik untuk foto adalah blue hour dan golden hour</li>
                    <li>Perhatikan skala dengan menambahkan objek pembanding</li>
                    <li>Gunakan hyperfocal distance untuk ketajaman maksimal</li>
                </ul>
            ''')
        elif prediction == "Sea":
            st.expander(f"Predicted Category: {prediction}").write('''
                Sea merupakan kategori yang menunjukkan bahwa objek tersebut adalah laut, yaitu badan air asin yang lebih kecil daripada samudra dan lebih besar daripada danau. Laut merupakan tempat kehidupan laut berkembang dan juga berfungsi sebagai penghubung antara berbagai ekosistem darat dan laut.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Golden Hour</strong>: Cahaya lembut akan memberikan warna yang hangat pada air laut dan langit. Gelombang yang pecah akan menciptakan efek yang dramatis.</li>
                                    <li><strong>Malam</strong>: Cahaya bulan yang memantul di permukaan air laut akan menciptakan suasana yang tenang dan misterius.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Laut").html('''
                <ul class="ul-content">
                    <li>Eksperimen dengan shutter speed untuk efek air yang berbeda</li>
                    <li>Lindungi kamera dari air laut dan pasir</li>
                    <li>Manfaatkan refleksi pada air untuk komposisi</li>
                    <li>Perhatikan garis horizon agar tetap lurus</li>
                    <li>Gunakan filter ND untuk long exposure di siang hari</li>
                </ul>
            ''')
        elif prediction == "Street":
            st.expander(f"Predicted Category: {prediction}").write('''
                Street merupakan kategori yang menunjukkan bahwa objek tersebut adalah jalan atau trotoar yang digunakan untuk lalu lintas kendaraan dan pejalan kaki. Jalan ini dapat ditemukan di daerah perkotaan dan menghubungkan berbagai area.
            ''')
            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>Cuaca yang Disarankan</strong>:</p>
                                <ul class="ul-content">
                                    <li><strong>Golden Hour</strong>: Cahaya lembut akan memberikan suasana yang hangat dan romantis pada foto jalanan. Bayangan panjang akan menambah dimensi pada bangunan dan orang-orang yang lewat.</li>
                                    <li><strong>Hujan</strong>: Hujan dapat menciptakan suasana yang unik dan dramatis pada foto jalanan. Perhatikan refleksi cahaya pada genangan air.</li>
                                </ul>
                            </div>
                        </div>
                    ''')
            display_weather_columns()
            st.expander("Ekstra Tips Untuk Menangkap Lanskap Jalan").html('''
                <ul class="ul-content">
                    <li>Gunakan mode aperture priority untuk respons cepat</li>
                    <li>Cari momen dan interaksi manusia yang menarik</li>
                    <li>Manfaatkan bayangan dan kontras untuk dramatisasi</li>
                    <li>Perhatikan komposisi dengan arsitektur sekitar</li>
                    <li>Praktikkan zone focusing untuk foto spontan</li>
                </ul>
            ''')