import streamlit as st
import os

def show_help():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)

    st.html('<p class="title-home">How to Use <span class="gradient">Classicape</span></p>')
    st.expander("Live Camera Prediction").write('''
        1. Klik opsi "Live Camera Prediction" pada Navigation Bar.
        2. Izinkan akses kamera pada perangkat Anda.
        3. Arahkan kamera ke gambar landscape yang ingin Anda klasifikasikan.
        4. Tekan "Capture Image" untuk mengambil gambar.
        5. The image will be captured and processed.
        6. Tunggu hingga proses selesai.
        7. Hasil klasifikasi akan ditampilkan di layar.
    ''')
    st.expander("Upload an Image").write('''
        1. Klik "Upload Image" pada Navigation Bar.
        2. Pilih opsi "Single Image" atau "Batch (ZIP)" sesuai kebutuhan Anda.
        > Single Image: Tekan Browse untuk memilih gambar landscape yang ingin Anda klasifikasikan lalu tekan "Upload Image" untuk mengunggah gambar. \n
        > Batch (ZIP): Tekan di bagian Container (kotak) untuk memilih ZIP file yang berisi gambar landscape yang ingin Anda klasifikasikan lalu masukkan nama yang nantinya menjadi nama folder ZIP hasil klasifikasi.
        3. The image will be uploaded and processed.
        4. Tunggu hingga proses selesai.
        5. ZIP file hasil klasifikasi akan ditampilkan di layar.
        6. Download ZIP file hasil klasifikasi.
    ''')
    st.html('<p class="title-home" style="margin-top: 20px;">FAQs About <span class="gradient">Classicape</span></p>')
    st.expander("Apa itu Classicape?").html("""
        <p class="paragraph-details">Classicape adalah aplikasi klasifikasi gambar yang menggunakan model deep learning untuk mengenali dan mengklasifikasikan foto landscape ke dalam enam kategori: Building, Forest, Glacier, Mountain, Sea, dan Street.</p>
    """)
    st.expander("Bagaimana Classicape bekerja?").html("""
        <p class="paragraph-details">Classicape menggunakan model deep learning ResNet50 yang telah dilatih pada dataset landscape untuk mengenali dan mengklasifikasikan gambar dengan akurasi tinggi.</p>
    """)
    st.expander("Apa tujuan dari Classicape?").html("""
        <p class="paragraph-details">Classicape bertujuan membantu pengguna, baik dalam edukasi, penelitian, maupun hobi, untuk dengan mudah mengelompokkan gambar landscape.</p>
    """)
    st.expander("Apa kategori gambar yang dapat dikenali oleh Classicape?").html("""
        <p class="paragraph-details">Kategori yang dapat dikenali adalah Building, Forest, Glacier, Mountain, Sea, dan Street.</p>
    """)
    st.expander("Apakah saya perlu koneksi internet untuk menggunakan Classicape?").html("""
        <p class="paragraph-details">Tidak, semua pemrosesan dilakukan secara lokal pada perangkat Anda tanpa memerlukan koneksi internet.</p>
    """)
    st.expander("Apakah Classicape dapat digunakan pada semua perangkat?").html("""
        <p class="paragraph-details">Classicape dirancang untuk kompatibel dengan berbagai perangkat, tetapi performa terbaik akan dirasakan pada perangkat dengan GPU yang memadai.</p>
    """)
    st.expander("Bagaimana keamanan data saya saat menggunakan Classicape?").html("""
        <p class="paragraph-details">Data gambar Anda akan dienkripsi dan disimpan di perangkat Anda secara lokal.</p>
    """)
    st.expander("Dapatkah saya mengunggah lebih dari satu gambar sekaligus?").html("""
        <p class="paragraph-details">Ya, Classicape mendukung unggahan gambar dalam batch menggunakan berkas zip.</p>
    """)
    st.expander("Seberapa akurat hasil prediksi Classicape?").html("""
        <p class="paragraph-details">Berdasarkan pengujian, Classicape memiliki akurasi keseluruhan 87% dengan hasil terbaik pada kategori forest (97% akurasi) dan sea (90% akurasi).</p>
        <pre class="paragraph-details color-pre">
    Classification Report:
                  precision    recall  f1-score   support

       buildings       0.90      0.84      0.87       437
          forest       0.97      0.98      0.97       474
         glacier       0.89      0.72      0.79       553
        mountain       0.77      0.82      0.80       525
             sea       0.84      0.97      0.90       510
          street       0.88      0.92      0.90       501

        accuracy                           0.87      3000
       macro avg       0.88      0.87      0.87      3000
    weighted avg       0.87      0.87      0.87      3000
        </pre>
    """)
    st.expander("Apa langkah berikutnya jika prediksi tidak sesuai?").html('''
        <p class="paragraph-details">Jika hasil prediksi tidak sesuai, Anda dapat mencoba mengunggah gambar dengan kualitas lebih baik atau pencahayaan yang memadai. Untuk pengembangan lanjutan, model dapat diperbarui dengan dataset tambahan.</p>
    ''')

    st.html('<p class="title-home" style="margin-top: 20px;">About <span class="gradient">Developer</span></p>')
    st.html('''
        <div class="container">
            <div class="container-content">
                <p style="font-size: 18px; text-align: center;"><strong>Travis Zusa Zuve Saputra</strong></p>
                <div style="text-align: center;">
                    <a href="https://github.com/traviszusa" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank"></a>
                    <a href="https://www.linkedin.com/in/traviszusa" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
                    <a href="https://instagram.com/trvs.z" target="_blank"><img src="https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white" target="_blank"></a>
                    <a href="https://discordapp.com/users/544152309320515585" target="_blank"><img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" target="_blank"></a>
                </div>
            </div>
        </div>
    ''')