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

            if image.mode == "RGBA":
                image = image.convert("RGB")

            predicted_class = predict_image(model, image)

            # Rename and save the image in the corresponding category folder
            new_name = f"{categories[predicted_class]}_{img_file.name}"
            new_path = os.path.join(output_dir, categories[predicted_class], new_name)
            image.save(new_path)

    # Create a ZIP file with classified images
    result_zip_path = os.path.join(output_dir, f"{zip_name}.zip")
    shutil.make_archive(result_zip_path.replace(".zip", ""), 'zip', output_dir)

    return result_zip_path

def display_edit_columns():
    st.html("<h2 class='sub-home'>Kunci Penting <span class='gradient'>Editing Foto</span></h2>")
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Brightness</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Digunakan untuk mengurangi area yang terlalu terang, seperti langit yang terlalu putih atau jendela yang terlalu silau. Digunakan untuk mengurangi area yang terlalu terang, seperti langit yang terlalu putih atau jendela yang terlalu silau.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Digunakan untuk mencerahkan area yang terlalu gelap, terutama pada bagian dalam bangunan atau area yang teduh.</p></li>
                        </ul>
                    </div>
                </div>
            ''')
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Contrast</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Membuat gambar terlihat lebih lembut dan halus. Cocok untuk gaya foto yang natural.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Membuat perbedaan antara area terang dan gelap lebih jelas, sehingga detail arsitektur lebih menonjol. Cocok untuk gaya foto yang dramatis.</p></li>
                        </ul>        
                    </div>    
                </div>
            ''')
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Highlight</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Membuat warna lebih cerah dan lebih lembut. Cocok untuk foto yang memiliki warna yang cerah dan lembut.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Membuat area terang lebih menonjol, namun hati-hati agar tidak kehilangan detail.</p></li>
                        </ul>
                    </div>
                </div>
            ''')
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Temperature</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Membuat gambar terlihat lebih dingin, dengan warna biru yang lebih dominan. Cocok untuk foto bangunan modern atau saat cuaca mendung.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Membuat gambar terlihat lebih hangat, dengan warna kuning atau oranye yang lebih dominan. Cocok untuk foto bangunan tua atau saat matahari terbenam.</p></li>
                        </ul>
                    </div>
                </div>
            ''')
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Vibrance</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Mengurangi saturasi warna secara keseluruhan, membuat gambar terlihat lebih lembut.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Meningkatkan saturasi warna pada area yang kurang jenuh, terutama pada warna kulit dan warna-warna pastel.</p></li>
                        </ul>
                    </div>
                </div>
            ''')
    st.html('''<div class="container">
                    <div class="container-content">
                        <p style="font-size: 18px; text-align: center;"><strong>Saturation</strong></p>
                        <ul class="ul-content">
                            <li><p class="zero-margin text-justify"><strong>Menurunkan</strong>: Mengurangi intensitas semua warna dalam gambar, membuat gambar terlihat lebih pudar.</p></li>
                            <li><p class="zero-margin text-justify"><strong>Meningkatkan</strong>: Meningkatkan intensitas semua warna dalam gambar. Cocok untuk gaya foto yang hidup dan penuh warna.</p></li>
                        </ul>
                    </div>
                </div>
            ''')

# Main function for the upload page
def show_upload():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)
    
    st.html('<p class="title-home">Upload <span class="gradient">Image</span></p>')

    # Load the model
    model = load_model()

    # Allow user to select the processing mode
    option = st.selectbox("Select processing mode:", ["Single Image", "Batch (ZIP)"])

    if option == "Single Image":
        # Single image upload
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)

            if image.mode == "RGBA":
                image = image.convert("RGB")

            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Perform prediction
            predicted_class = predict_image(model, image)
            categories = ["Building", "Forest", "Glacier", "Mountain", "Sea", "Street"]
            if categories[predicted_class] == "Building":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Building merupakan kategori yang menunjukkan bahwa objek tersebut merupakan bangunan maupun gedung, sehingga dapat diidentifikasi sebagai objek bangunan."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap Bangunan").html('''
                    <ul class="ul-content-2">
                        <li><strong>Perhatikan Perspektif</strong>: Bangunan seringkali memiliki garis-garis lurus yang kuat. Pastikan garis-garis ini benar-benar lurus saat diedit. Gunakan tools seperti "Perspective Correction" untuk memperbaiki distorsi perspektif jika diperlukan.</li>
                        <li><strong>Tingkatkan Detail Arsitektur</strong>: Gunakan tools seperti "Sharpen" atau "Clarity" untuk menonjolkan detail arsitektur seperti ukiran, ornamen, atau tekstur batu bata. Namun, jangan berlebihan agar tidak terlihat terlalu tajam dan artificial.</li>
                        <li><strong>Buat Suasana dengan Warna</strong>: Warna dapat sangat mempengaruhi suasana foto. Misalnya, warna hangat (kuning, oranye) dapat memberikan kesan hangat dan nyaman, sedangkan warna dingin (biru, ungu) bisa memberikan kesan misterius.</li>
                        <li><strong>Pertimbangkan Black and White</strong>: Tidak semua foto bangunan harus berwarna. Terkadang, mengubah foto menjadi hitam putih dapat memberikan kesan klasik dan elegan, terutama untuk bangunan bersejarah.</li>
                        <li><strong>Eksperimen dengan Vignette dan Grain</strong>: Vignette dapat membantu mengarahkan perhatian ke subjek utama, sedangkan grain (noise) dapat memberikan kesan film klasik. Gunakan kedua efek ini secara hati-hati agar tidak berlebihan.</li>
                    </ul>
                ''')
            elif categories[predicted_class] == "Forest":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Forest merupakan kategori yang menunjukkan bahwa objek tersebut adalah hutan atau area hijau alami yang terdiri dari pepohonan, semak, dan ekosistem yang mendukung kehidupan flora dan fauna. Kategori ini mengindikasikan bahwa lingkungan yang terdeteksi termasuk dalam wilayah hutan."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap ").html('''
                    <ul class="ul-content-2">
                        <li><strong>Perhatikan Keseimbangan Warna</strong>: Hutan identik dengan warna hijau. Namun, jangan ragu untuk bermain dengan warna lain seperti cokelat batang pohon, kuning dedaunan kering, atau biru langit. Pastikan warna-warna ini saling melengkapi dan tidak terlalu mencolok.</li>
                        <li><strong>Tingkatkan Detail Tekstur</strong>: Untuk menonjolkan tekstur kulit pohon, dedaunan, atau lumut, gunakan tools seperti sharpen atau clarity. Namun, jangan berlebihan agar hasilnya tidak terlihat terlalu tajam dan artificial.</li>
                        <li><strong>Buat Vignette</strong>: Vignette adalah efek menggelapkan tepi foto secara perlahan. Efek ini dapat membantu mengarahkan perhatian ke subjek utama dan memberikan kesan kedalaman pada foto.</li>
                        <li><strong>Pertimbangkan Black and White</strong>: Terkadang, mengubah foto hutan menjadi hitam putih dapat memberikan kesan dramatis dan artistik. Cobalah bereksperimen dengan berbagai preset black and white untuk menemukan yang paling sesuai.</li>
                        <li><strong>Jangan Takut Berkreasi</strong>: Pengeditan foto adalah seni. Jangan terpaku pada satu gaya tertentu. Cobalah berbagai teknik dan filter untuk menemukan gaya yang paling sesuai dengan kepribadianmu.</li>
                    </ul>
                ''')
            elif categories[predicted_class] == "Glacier":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Glacier merupakan kategori yang menunjukkan bahwa objek tersebut adalah gletser atau lapisan es yang luas, yang biasanya terdapat di daerah pegunungan tinggi atau kutub. Gletser ini mencair dan membentuk aliran air yang mengalir ke laut."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap ").html('''
                    <ul class="ul-content-2">
                        <li><strong>Tingkatkan Warna Biru Es</strong>: Gletser dikenal dengan warna birunya yang khas. Untuk menonjolkan warna ini, kamu bisa sedikit menaikkan saturasi warna biru dan mengurangi saturasi warna lainnya. Hati-hati agar tidak membuat warna menjadi terlalu jenuh.</li>
                        <li><strong>Perhatikan Tekstur Es</strong>: Gletser memiliki tekstur yang unik, dari retakan halus hingga bongkahan es yang besar. Gunakan tools seperti "sharpen" atau "clarity" untuk menonjolkan tekstur ini. Namun, jangan berlebihan agar tidak terlihat terlalu noise.</li>
                        <li><strong>Buat Suasana Dingin</strong>: Untuk menciptakan suasana dingin dan sejuk, kamu bisa sedikit menurunkan suhu warna (menjadi lebih kebiruan) dan mengurangi vibrance.</li>
                        <li><strong>Pertimbangkan Black and White</strong>: Terkadang, mengubah foto gletser menjadi hitam putih dapat memberikan kesan dramatis dan artistik. Cobalah bereksperimen dengan berbagai preset black and white untuk menemukan yang paling sesuai.</li>
                        <li><strong>Eksperimen dengan Tone Mapping</strong>: Tone mapping adalah teknik yang berguna untuk meningkatkan detail pada area terang dan gelap dalam foto. Ini sangat berguna untuk foto gletser yang memiliki kontras yang tinggi.</li>
                    </ul>
                ''')
            elif categories[predicted_class] == "Mountain":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Mountain merupakan kategori yang menunjukkan bahwa objek tersebut adalah gunung, biasanya berupa struktur geologis yang lebih tinggi dari sekitarnya. Gunung dapat berupa puncak tajam atau lebih landai dan ditemukan di seluruh dunia."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap ").html('''
                    <ul class="ul-content-2">
                        <li><strong>Tingkatkan Kedalaman Lapisan</strong>: Gunung seringkali memiliki banyak lapisan, mulai dari rerumputan di bawah hingga puncak yang tertutup salju. Untuk menekankan kedalaman ini, kamu bisa bermain dengan kontras. Naikkan sedikit kontras pada lapisan yang lebih dekat dengan kamera dan turunkan sedikit kontras pada lapisan yang lebih jauh. Ini akan menciptakan ilusi kedalaman.</li>
                        <li><strong>Perhatikan Keseimbangan Warna</strong>: Gunung biasanya memiliki palet warna yang terbatas, seperti hijau, cokelat, dan abu-abu. Namun, jangan ragu untuk sedikit bermain dengan warna. Misalnya, kamu bisa sedikit menaikkan saturasi warna hijau pada pepohonan atau warna biru pada langit untuk memberikan kesan yang lebih hidup.</li>
                        <li><strong>Buat Suasana Dramatis</strong>: Untuk menciptakan suasana dramatis, kamu bisa menggunakan teknik seperti HDR (High Dynamic Range) atau tone mapping. Teknik ini akan membantu meningkatkan detail pada area terang dan gelap, sehingga membuat foto terlihat lebih dramatis.</li>
                        <li><strong>Pertimbangkan Vignette dan Grain</strong>: Vignette dapat membantu mengarahkan perhatian ke subjek utama, sedangkan grain (noise) dapat memberikan kesan film klasik. Gunakan kedua efek ini secara hati-hati agar tidak berlebihan.</li>
                        <li><strong>Eksperimen dengan Filter Hitam Putih</strong>: Tidak semua foto gunung harus berwarna. Terkadang, mengubah foto menjadi hitam putih dapat memberikan kesan klasik dan elegan, terutama untuk foto gunung yang berkabut atau saat matahari terbit/terbenam.</li>
                    </ul>
                ''')
            elif categories[predicted_class] == "Sea":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Sea merupakan kategori yang menunjukkan bahwa objek tersebut adalah laut, yaitu badan air asin yang lebih kecil daripada samudra dan lebih besar daripada danau. Laut merupakan tempat kehidupan laut berkembang dan juga berfungsi sebagai penghubung antara berbagai ekosistem darat dan laut."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap ").html('''
                    <ul class="ul-content-2">
                        <li><strong>Tingkatkan Warna Biru Laut</strong>: Laut identik dengan warna biru yang luas. Untuk menonjolkan warna ini, kamu bisa sedikit menaikkan saturasi warna biru dan mengurangi saturasi warna lainnya. Hati-hati agar tidak membuat warna menjadi terlalu jenuh. Kamu juga bisa bermain dengan tone warna untuk mendapatkan efek yang berbeda-beda, misalnya warna biru kehijauan atau biru tua yang misterius.</li>
                        <li><strong>Perhatikan Tekstur Ombak</strong>: Ombak memiliki tekstur yang dinamis dan menarik. Gunakan tools seperti "sharpen" atau "clarity" untuk menonjolkan tekstur ini. Namun, jangan berlebihan agar tidak terlihat terlalu noise.</li>
                        <li><strong>Buat Suasana Dingin dan Segar</strong>: Untuk menciptakan suasana dingin dan segar, kamu bisa sedikit menurunkan suhu warna (menjadi lebih kebiruan) dan mengurangi vibrance. Selain itu, kamu bisa menambahkan sedikit efek "fog" atau kabut untuk memberikan kesan misterius.</li>
                        <li><strong>Pertimbangkan Black and White</strong>: Terkadang, mengubah foto laut menjadi hitam putih dapat memberikan kesan dramatis dan artistik. Cobalah bereksperimen dengan berbagai preset black and white untuk menemukan yang paling sesuai. Misalnya, untuk menciptakan suasana yang dramatis, kamu bisa mencoba preset high contrast.</li>
                        <li><strong>Eksperimen dengan Tone Mapping</strong>: Tone mapping adalah teknik yang berguna untuk meningkatkan detail pada area terang dan gelap dalam foto. Ini sangat berguna untuk foto laut yang memiliki kontras yang tinggi, misalnya saat memotret matahari terbit atau terbenam.
                    </ul>
                ''')
            elif categories[predicted_class] == "Street":
                st.expander(f"Predicted Category: {categories[predicted_class]}").write(
                    "Street merupakan kategori yang menunjukkan bahwa objek tersebut adalah jalan atau trotoar yang digunakan untuk lalu lintas kendaraan dan pejalan kaki. Jalan ini dapat ditemukan di daerah perkotaan dan menghubungkan berbagai area."
                )
                display_edit_columns()
                st.expander("Ekstra Tips Untuk Mengedit Lanskap ").html('''
                    <ul class="ul-content-2">
                        <li><strong>Perhatikan Keseimbangan Warna</strong>: Foto jalanan seringkali memiliki banyak elemen warna yang berbeda-beda. Pastikan warna-warna ini saling melengkapi dan tidak terlalu mencolok. Kamu bisa menggunakan tools seperti "color grading" untuk mengatur keseimbangan warna secara keseluruhan.</li>
                        <li><strong>Tingkatkan Kontras</strong>: Untuk membuat foto jalanan terlihat lebih dramatis, kamu bisa sedikit menaikkan kontras. Ini akan membuat warna-warna menjadi lebih tajam dan detail arsitektur menjadi lebih menonjol.</li>
                        <li><strong>Buat Suasana dengan Vignette</strong>: Vignette dapat membantu mengarahkan perhatian ke subjek utama dan memberikan kesan kedalaman pada foto. Selain itu, vignette juga bisa membantu menciptakan suasana yang lebih intim.</li>
                        <li><strong>Pertimbangkan Black and White</strong>: Terkadang, mengubah foto jalanan menjadi hitam putih dapat memberikan kesan klasik dan artistik. Cobalah bereksperimen dengan berbagai preset black and white untuk menemukan yang paling sesuai.</li>
                        <li><strong>Eksperimen dengan Grain</strong>: Grain (noise) dapat memberikan kesan film klasik pada foto. Gunakan efek ini secara hati-hati agar tidak berlebihan.</li>
                    </ul>
                ''')

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

            st.html('''<div class="container">
                            <div class="container-content">
                                <p class="zero-margin text-justify"><strong>ZIP Sedang di Proses</strong></p></li>
                            </div>
                        </div>
                    ''')
            
            # Offer the result ZIP file for download
            with open(result_zip, "rb") as f:
                st.download_button(
                    label="Download Classified Images ZIP",
                    data=f,
                    file_name=f"{zip_name}.zip",
                    mime="application/zip"
                )