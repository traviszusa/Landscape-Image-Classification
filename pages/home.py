import streamlit as st
import os

def show_home():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(parent_dir, "../resources/images/thumbnail.jpg")
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)
    
    st.html('<p class="title-home">Selamat Datang di <span class="gradient">Classicape</span></p>')

    st.image(image_path, caption="Classicape Logo")

    st.html('<div class="container"><p class="container-content text-justify"><strong>Classicape</strong> adalah aplikasi web berbasis machine learning yang dirancang untuk mengklasifikasikan foto ke dalam enam kategori landscape yang berbeda</p></div>')
    col1, col2 = st.columns([2, 1])

    with col1:
        st.html('''<div class="container">
                        <div class="container-content">
                            <p style="font-size: 18px;"><strong>Kategori Klasifikasi:</strong></p>
                            <ul class="ul-content">
                                <li><strong>Building</strong>: Gedung dan Bangunan</li>
                                <li><strong>Forest</strong>: Hutan dan Hijauan</li>
                                <li><strong>Glacier</strong>: Gletser dan Bongkahan Es</li>
                                <li><strong>Mountain</strong>: Gunung dan Pegunungan</li>
                                <li><strong>Sea</strong>: Laut dan Pantai</li>
                                <li><strong>Street</strong>: Jalan</li>
                            </ul>
                            <p class="note">Sebagai catatan, klasifikasi di atas didasarkan pada dataset yang tersedia, model dapat dilakukan train ulang untuk menambahkan kategori klasifikasi baru</p>
                        </div>
                    </div>''')
        
    with col2:
        st.html('''<div class="container">
                        <div class="container-content">
                            <p style="font-size: 18px;"><strong>Alat yang Digunakan:</strong></p>
                            <ul class="ul-content">
                                <li><a href="https://code.visualstudio.com/" target="_blank" style="text-decoration: none;">Visual Studio Code</a></li>
                                <li><a href="https://streamlit.io/" target="_blank" style="text-decoration: none;">Streamlit</a></li>
                                <li><a href="https://pytorch.org/hub/pytorch_vision_wide_resnet/" target="_blank" style="text-decoration: none;">Wide ResNet 50</a></li>
                                <li><a href="https://www.kaggle.com/datasets/puneet6060/intel-image-classification/" target="_blank" style="text-decoration: none;">Kaggle Dataset</a></li>
                                <li><a href="https://github.com/traviszusa/Landscape-Image-Classification" target="_blank" style="text-decoration: none;">GitHub</a></li>
                                <li><a href="https://www.nvidia.com/en-us/cuda-toolkit/" target="_blank" style="text-decoration: none;">Nvidia CUDA Toolkit</a></li>
                                <li><a href="https://pytorch.org/" target="_blank" style="text-decoration: none;">PyTorch</a></li>
                                <li><a href="https://www.python.org/" target="_blank" style="text-decoration: none;">Python</a></li>
                            </ul>
                        </div>
                    </div>''')