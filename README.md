# Face Mask Detection

Proyek ini bertujuan untuk membangun sebuah sistem cerdas yang dapat secara otomatis mendeteksi apakah seseorang memakai masker atau tidak menggunakan deep learning dan OpenCV. Sistem ini bekerja dengan cara mengambil input berupa gambar atau video secara real-time, kemudian memprosesnya untuk mendeteksi keberadaan wajah serta mengklasifikasikan apakah wajah tersebut memakai masker dengan benar, tidak memakai masker, atau memakai masker secara tidak tepat. Untuk mendukung proyek ini, digunakan dataset Face Mask 12K Images Dataset yang tersedia di Kaggle melalui tautan berikut: https://www.kaggle.com/datasets/ashishjangra27/face-mask-12k-images-dataset. Dataset ini berisi sekitar 12.000 gambar yang telah dikategorikan menjadi tiga kelas utama, yaitu dengan masker, tanpa masker, dan memakai masker secara tidak benar.

Proses pengembangan sistem dimulai dari pengumpulan dan pra-pemrosesan data, seperti melakukan deteksi wajah dengan OpenCV, resize gambar ke ukuran tertentu (misalnya 224x224 piksel), normalisasi nilai pixel, serta augmentasi data untuk meningkatkan variasi gambar. Selanjutnya, model deep learning berbasis Convolutional Neural Network (CNN) dibangun untuk mengklasifikasikan gambar wajah tersebut. Model dapat dibuat dari awal atau menggunakan model pretrained seperti MobileNetV2 agar pelatihan lebih cepat dan akurat. Setelah model terlatih, dilakukan integrasi dengan OpenCV untuk memungkinkan deteksi wajah dan klasifikasi secara real-time menggunakan input dari kamera atau webcam.

Pada tahap akhir, sistem diuji dan dievaluasi menggunakan metrik seperti akurasi, precision, recall, serta analisis confusion matrix untuk mengetahui sejauh mana kemampuan model membedakan ketiga kelas tersebut. Output dari proyek ini adalah sebuah aplikasi yang mampu mendeteksi wajah dan memberikan notifikasi visual, misalnya dengan menampilkan kotak berwarna hijau untuk wajah yang memakai masker dengan benar, kotak merah untuk wajah tanpa masker, serta indikasi khusus untuk pemakaian masker yang salah. Teknologi utama yang digunakan dalam proyek ini meliputi Python sebagai bahasa pemrograman, serta library seperti TensorFlow/Keras untuk deep learning, OpenCV untuk pemrosesan gambar dan video, serta NumPy dan Matplotlib untuk manipulasi data dan visualisasi.

## Persyaratan
Pastikan Anda telah menginstal dependensi yang diperlukan sebelum menjalankan proyek. Semua dependensi tercantum dalam file `requirements.txt`.

## Instalasi
Jalankan perintah berikut untuk menginstal semua dependensi yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## Cara Menggunakan
1. Jalankan skrip deteksi dengan perintah:
   ```bash
   python detect_mask.py
   ```
2. Kamera akan terbuka dan mulai mendeteksi wajah serta apakah seseorang memakai masker atau tidak.

## File dan Struktur
- `detect_mask.py`: Skrip utama untuk mendeteksi masker.
- `model.h5`: Model deep learning yang digunakan.
- `requirements.txt`: Daftar dependensi yang diperlukan.
- `README.md`: Dokumentasi proyek ini.

## Dependensi
opencv-python
tensorflow
numpy
matplotlib

## Kontributor
- RAHMAT HIDAYAT

## Lisensi
Proyek ini berlisensi di bawah MIT License.
