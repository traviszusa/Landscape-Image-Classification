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
    
    st.html('<p class="title-home">Selamat Datang di <a class="gradient">Classicape</a></p>')

    st.image(image_path, caption="Classicape Logo")

    st.write("""
    Classicape adalah aplikasi berbasis machine learning yang dirancang untuk mengklasifikasikan foto 
    ke dalam enam kategori landscape yang berbeda:
    
    - **Building**: Menampilkan gambar bangunan atau struktur buatan manusia.
    - **Forest**: Mengklasifikasikan gambar yang menunjukkan pemandangan hutan atau vegetasi lebat.
    - **Glacier**: Gambar yang mengandung gletser atau lapisan es besar.
    - **Mountain**: Menampilkan pemandangan pegunungan atau formasi batuan tinggi.
    - **Sea**: Gambar yang berisi lautan atau pemandangan pantai.
    - **Street**: Gambar yang menunjukkan jalan atau area perkotaan.
    
    Dengan menggunakan model *deep learning* yang telah dilatih menggunakan dataset besar, aplikasi ini 
    dapat memberikan hasil klasifikasi yang sangat akurat dan cepat. 
    Cukup unggah gambar Anda dan biarkan model kami bekerja!
    """)
    
    st.write("""
    Pada halaman ini, Anda dapat mengeksplorasi informasi lebih lanjut tentang fitur aplikasi 
    atau melanjutkan untuk mencoba fitur klasifikasi gambar.
    """)