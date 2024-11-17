import streamlit as st
import os

def show_about():
    def load_css(file_path):
        with open(file_path) as f:
            st.html(f"<style>{f.read()}</style>")
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(parent_dir, "../resources/css/style.css")
    load_css(css_path)

    st.html('''
    <p class="title-home">About <a class="gradient">Classicape</a></p>
    <details>
        <summary>Apa itu Classicape?</summary>
        <p class="paragraph-details">Classicape adalah aplikasi klasifikasi gambar yang menggunakan model deep learning untuk mengenali dan mengklasifikasikan foto landscape ke dalam enam kategori: Building, Forest, Glacier, Mountain, Sea, dan Street.</p>
    </details>
    <details>
        <summary>Bagaimana cara Classicape bekerja?</summary>
        <p class="paragraph-details">Classicape menggunakan model deep learning ResNet50 yang telah dilatih pada dataset landscape untuk mengenali dan mengklasifikasikan gambar dengan akurasi tinggi.</p>
    </details>
    <details>
        <summary>Apa tujuan dari Classicape?</summary>
        <p class="paragraph-details">Classicape bertujuan membantu pengguna, baik dalam edukasi, penelitian, maupun hobi, untuk dengan mudah mengelompokkan gambar landscape.</p>
    </details>
    <details>
        <summary>Apa kategori gambar yang dapat dikenali oleh Classicape?</summary>
        <p class="paragraph-details">Kategori yang dapat dikenali adalah Building, Forest, Glacier, Mountain, Sea, dan Street.</p>
    </details>
    <details>
        <summary>Apakah saya perlu koneksi internet untuk menggunakan Classicape?</summary>
        <p class="paragraph-details">Tidak, semua pemrosesan dilakukan secara lokal pada perangkat Anda tanpa memerlukan koneksi internet.</p>
    </details>
    <details>
        <summary>Apakah Classicape dapat digunakan pada semua perangkat?</summary>
        <p class="paragraph-details">Classicape dirancang untuk kompatibel dengan berbagai perangkat, tetapi performa terbaik akan dirasakan pada perangkat dengan GPU yang memadai.</p>
    </details>
    <details>
        <summary>Bagaimana keamanan data saya saat menggunakan Classicape?</summary>
        <p class="paragraph-details"> Gambar yang diunggah tidak disimpan di server. Semua data hanya diproses secara lokal untuk menjaga privasi pengguna.</p>
    </details>
    <details>
        <summary>Dapatkah saya mengunggah lebih dari satu gambar sekaligus?</summary>
        <p class="paragraph-details">Ya, Classicape mendukung unggahan gambar dalam batch menggunakan berkas zip.</p>
    </details>
    <details>
        <summary>Seberapa akurat hasil prediksi Classicape?</summary>
        <p class="paragraph-details">Berdasarkan pengujian, Classicape memiliki akurasi keseluruhan 87% dengan hasil terbaik pada kategori forest (97% akurasi) dan sea (90% akurasi).</p>
        <pre class="paragraph-details">
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
    </details>
    <details>
        <summary>Apa langkah berikutnya jika prediksi tidak sesuai?</summary>
        <p class="paragraph-details">Jika hasil prediksi tidak sesuai, Anda dapat mencoba mengunggah gambar dengan kualitas lebih baik atau pencahayaan yang memadai. Untuk pengembangan lanjutan, model dapat diperbarui dengan dataset tambahan.</p>
    </details>
    ''')