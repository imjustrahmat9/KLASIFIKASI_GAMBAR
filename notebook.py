## Import Semua Packages/Library yang Digunakan
"""

!pip install -q kaggle

!pip install split-folders

!pip install tensorflow==2.18.0
!pip install tensorflow-decision-forests==1.11.0  # Versi sebelum 1.12.0
!pip install tf-keras==2.18.0  # Versi sebelum 2.19.0

!pip install tensorflowjs

"""Melakukan import library yang digunakan untuk keseluruhan proyek."""

import os  # Modul untuk berinteraksi dengan sistem operasi, seperti membaca dan menulis file
import splitfolders  # Digunakan untuk membagi dataset gambar ke dalam folder train, val, dan test secara otomatis
import tensorflow as tf  # Library utama untuk deep learning
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # Modul untuk augmentasi dan preprocessing gambar
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten  # Lapisan-lapisan utama dalam CNN
from keras.models import Sequential  # Model sekuensial untuk membangun arsitektur CNN
from keras.preprocessing import image  # Modul untuk memuat dan memproses gambar individu
import matplotlib.pyplot as plt  # Modul untuk visualisasi data, seperti menampilkan gambar dan grafik
import numpy as np  # Library untuk operasi numerik, seperti manipulasi array
from PIL import Image  # Modul untuk membuka dan memproses gambar
import random  # Modul untuk operasi acak, seperti memilih gambar secara random
import shutil  # Modul untuk operasi file dan direktori, seperti menyalin atau memindahkan file
from tensorflow.keras.applications import MobileNetV2  # Model MobileNetV2 yang sudah dilatih sebelumnya, digunakan untuk transfer learning
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping  # Callback untuk menyimpan model terbaik dan menghentikan pelatihan jika tidak ada peningkatan

"""Mengambil API Kaggle untuk mendapatkan dataset"""

# Menggunakan variabel lingkungan dengan aman
os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME")
os.environ["KAGGLE_KEY"] = os.getenv("KAGGLE_KEY")

"""Melakukan cek version tensorflow"""

print(f'TensorFlow version: {tf.__version__}')

"""Dataset original bersumber dari [Kaggle](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)."""

!kaggle datasets download -d vipoooool/new-plant-diseases-dataset

"""Melakukan unzip terhadap file."""

!unzip new-plant-diseases-dataset.zip

"""# Data Preparation

### Data Loading

Membuat fungsi untuk menampilkan jumlah gambar dari masing-masing kelas dan menghitung jumlah gambar dengan resolusi tertentu.
"""

def count_images_and_resolution(base_path, target_resolution=None):
    # Dictionary untuk menyimpan jumlah gambar per kelas
    class_count = {}

    # Dictionary untuk menyimpan jumlah gambar per resolusi
    resolution_count = {}

    # Melakukan iterasi pada setiap folder dan file dalam base_path
    for root, dirs, files in os.walk(base_path):
        # Mengabaikan folder root utama karena tidak mewakili kelas tertentu
        if root == base_path:
            continue

        # Mengambil nama kelas dari nama folder
        class_name = os.path.basename(root)

        # Menyimpan jumlah gambar dalam kelas tersebut
        class_count[class_name] = len(files)

        # Iterasi melalui setiap file dalam folder kelas
        for file in files:
            file_path = os.path.join(root, file)  # Mendapatkan path lengkap file

            # Membuka gambar untuk mendapatkan resolusinya
            with Image.open(file_path) as img:
                width, height = img.size  # Mendapatkan ukuran gambar (lebar x tinggi)
                resolution = f"{width}x{height}"  # Format resolusi sebagai string (contoh: "256x256")

                # Jika resolusi belum ada dalam dictionary, inisialisasi dengan nilai 0
                if resolution not in resolution_count:
                    resolution_count[resolution] = 0

                # Menambahkan jumlah gambar dengan resolusi tersebut
                resolution_count[resolution] += 1

                # Jika ada resolusi target yang ingin dihitung secara spesifik
                if target_resolution and resolution == target_resolution:
                    if 'target' not in resolution_count:
                        resolution_count['target'] = 0
                    resolution_count['target'] += 1  # Menambahkan jumlah gambar dengan resolusi target

    return class_count, resolution_count  # Mengembalikan hasil dalam bentuk dictionary

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Resolusi spesifik yang ingin dihitung jumlahnya
target_resolution = "256x256"

# Memanggil fungsi untuk menghitung jumlah gambar berdasarkan kelas dan resolusi
class_count, resolution_count = count_images_and_resolution(base_path, target_resolution)

# Menampilkan jumlah gambar per kelas
print("Jumlah gambar per kelas:")
for class_name, count in class_count.items():
    print(f"{class_name}: {count}")

# Menampilkan jumlah gambar berdasarkan resolusi
print("\nJumlah gambar per resolusi:")
for resolution, count in resolution_count.items():
    print(f"{resolution}: {count}")

"""Terdapat 87867 gambar yang terbagi menjadi 38 kelas berbeda. Setiap gambar di masing-masing kelas memiliki resolusi 256x256.

Gambar diubah dengan resolusi antara 200 hingga 256. Gambar original akan ditimpa oleh gambar yang resolusi nya telah diubah sehingga tidak menambah jumlah dataset.
"""

def resize_and_replace_images(base_path, min_res=200, max_res=256):
    # Iterasi melalui setiap folder dan file dalam base_path
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)  # Mendapatkan path lengkap file

            try:
                # Membuka gambar
                with Image.open(file_path) as img:
                    # Menentukan ukuran baru secara acak dalam rentang yang diberikan
                    new_width = random.randint(min_res, max_res)
                    new_height = random.randint(min_res, max_res)

                    # Mengubah ukuran gambar sesuai ukuran baru
                    resized_img = img.resize((new_width, new_height))

                    # Jika gambar dalam mode RGBA tetapi disimpan sebagai JPEG, konversi ke RGB
                    if img.mode == "RGBA" and file_path.lower().endswith(".jpg"):
                        resized_img = resized_img.convert("RGB")

                    # Menyimpan gambar kembali ke lokasi yang sama (menggantikan gambar asli)
                    resized_img.save(file_path)

            except (IOError, OSError) as e:
                # Menangkap kesalahan yang terjadi saat membuka atau memproses gambar
                print(f"Error processing {file_path}: {e}")

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Memanggil fungsi untuk mengubah ukuran dan mengganti gambar dalam dataset
resize_and_replace_images(base_path)

"""Menampilkan kembali jumlah gambar untuk masing-masing resolusi."""

def count_images_and_resolution(base_path, target_resolution=None):
    class_count = {}  # Menyimpan jumlah gambar per kelas
    resolution_count = {}  # Menyimpan jumlah gambar per resolusi

    for root, dirs, files in os.walk(base_path):
        if root == base_path:  # Lewati folder root utama
            continue
        class_name = os.path.basename(root)
        class_count[class_name] = len(files)  # Hitung jumlah gambar per kelas

        for file in files:
            file_path = os.path.join(root, file)
            with Image.open(file_path) as img:
                width, height = img.size
                resolution = f"{width}x{height}"

                if resolution not in resolution_count:
                    resolution_count[resolution] = 0  # Inisialisasi jika belum ada

                resolution_count[resolution] += 1  # Tambah jumlah gambar dengan resolusi tersebut

                if target_resolution and resolution == target_resolution:
                    if 'target' not in resolution_count:
                        resolution_count['target'] = 0
                    resolution_count['target'] += 1  # Hitung gambar dengan resolusi target

    return class_count, resolution_count  # Kembalikan hasil perhitungan

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Resolusi yang ingin dihitung
target_resolution = "256x256"

class_count, resolution_count = count_images_and_resolution(base_path, target_resolution)

print("\nJumlah gambar per resolusi:")
for resolution, count in resolution_count.items():
    print(f"{resolution}: {count}")  # Cetak jumlah gambar per resolusi

"""### Data Preprocessing

Secara total terdapat 38 jenis tanaman yang berbeda. Namun pada proyek kali ini akan fokus ke tanaman tomat karena jumlah gambar lebih dari 10.000
"""

def count_images(base_path, target_classes=["Tomato"]):
    total_count = 0  # Inisialisasi total jumlah gambar
    class_counts = {cls: 0 for cls in target_classes}  # Inisialisasi jumlah gambar per kelas target

    for root, dirs, files in os.walk(base_path):
        total_count += len(files)  # Tambahkan jumlah gambar di setiap folder
        for cls in target_classes:
            if cls.lower() in root.lower():  # Periksa apakah nama kelas ada di path folder
                class_counts[cls] += len(files)  # Tambahkan jumlah gambar ke kelas yang sesuai

    return total_count, class_counts  # Kembalikan total gambar dan jumlah per kelas target

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Hitung jumlah gambar dalam dataset
total_count, class_counts = count_images(base_path)

# Tampilkan hasil perhitungan
print(f"Jumlah total gambar dalam dataset: {total_count}")
for cls, count in class_counts.items():
    print(f"Jumlah gambar dalam kelas '{cls}': {count}")  # Cetak jumlah gambar per kelas target

"""Menampilkan jumlah gambar untuk masing-masing subkelas dari tanaman tomat."""

def count_tomato_images_per_subclass(base_path, target_class="Tomato"):
    class_count = {}  # Inisialisasi dictionary untuk menyimpan jumlah gambar per subkelas

    for root, dirs, files in os.walk(base_path):
        if target_class.lower() in root.lower():  # Cek apakah folder mengandung nama kelas target
            subclass_name = os.path.basename(root)  # Ambil nama subkelas dari folder
            if subclass_name not in class_count:
                class_count[subclass_name] = 0  # Inisialisasi jika belum ada
            class_count[subclass_name] += len(files)  # Tambahkan jumlah gambar dalam subkelas

    return class_count  # Kembalikan jumlah gambar per subkelas

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Hitung jumlah gambar untuk subkelas dalam kelas "Tomato"
tomato_class_count = count_tomato_images_per_subclass(base_path)

# Menampilkan hasil
print("Jumlah gambar Tomato dari masing-masing subkelas:")
for subclass, count in tomato_class_count.items():
    print(f"{subclass}: {count}")  # Cetak jumlah gambar per subkelas

"""Memindahkan folder tanaman tomat dari /New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented) ke /Tomato"""

def copy_tomato_folders(base_path, target_folder="Tomato", target_class="tomato"):
    if not os.path.exists(target_folder):  # Periksa apakah folder tujuan sudah ada
        os.makedirs(target_folder)  # Buat folder tujuan jika belum ada

    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if target_class.lower() in dir_name.lower():  # Cek apakah folder mengandung nama "tomato"
                source_path = os.path.join(root, dir_name)  # Path folder sumber
                dest_path = os.path.join(target_folder, dir_name)  # Path folder tujuan
                if not os.path.exists(dest_path):  # Cek apakah folder tujuan sudah ada
                    shutil.copytree(source_path, dest_path)  # Salin seluruh folder
                    print(f"Menyalin {source_path} ke {dest_path}")  # Cetak status penyalinan

# Path ke folder utama dataset
base_path = "/content/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"

# Path ke folder tujuan untuk menyimpan data Tomato
target_folder = "/content/Tomato"

# Menyalin folder yang mengandung "Tomato"
copy_tomato_folders(base_path, target_folder)

"""Menghapus nama file"tomato___"."""

def rename_folders(base_path, prefix="Tomato___"):
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.startswith(prefix):  # Periksa apakah nama folder dimulai dengan prefix
                new_dir_name = dir_name[len(prefix):]  # Hapus prefix dari nama folder
                old_path = os.path.join(root, dir_name)  # Path lama folder
                new_path = os.path.join(root, new_dir_name)  # Path baru tanpa prefix
                os.rename(old_path, new_path)  # Ganti nama folder
                print(f"Renamed {old_path} to {new_path}")  # Cetak status perubahan

# Path ke folder utama yang berisi folder Tomato
base_path = "/content/Tomato"

# Jalankan fungsi untuk mengganti nama folder
rename_folders(base_path)

"""Menampilkan contoh gambar dari masing-masing kelas tomat."""

def show_example_images(base_path):
    class_images = {}  # Dictionary untuk menyimpan contoh gambar per kelas

    for root, dirs, files in os.walk(base_path):
        if files:  # Periksa apakah folder memiliki file gambar
            class_name = os.path.basename(root)  # Ambil nama kelas dari folder
            random_image = random.choice(files)  # Pilih satu gambar secara acak
            class_images[class_name] = os.path.join(root, random_image)  # Simpan path gambar

    fig, axes = plt.subplots(1, len(class_images), figsize=(15, 5))  # Buat subplot dengan jumlah kelas
    fig.suptitle('Contoh Gambar dari Masing-Masing Kelas')  # Judul grafik

    for ax, (class_name, image_path) in zip(axes, class_images.items()):
        img = Image.open(image_path)  # Buka gambar
        ax.imshow(img)  # Tampilkan gambar
        ax.text(0.5, -0.1, class_name, rotation=90, verticalalignment='top', horizontalalignment='center', transform=ax.transAxes)  # Tambahkan label kelas
        ax.axis('off')  # Sembunyikan axis

    plt.show()  # Tampilkan plot

# Path ke folder utama yang berisi dataset
base_path = "/content/Tomato"

# Jalankan fungsi untuk menampilkan contoh gambar
show_example_images(base_path)

"""#### Split Dataset

Pada proyek dicoding jumlah dataset minimal yang dibutuhkan adalah 10.000 sehingga pada proyek kali ini hanya akan dipilih 5 kelas saja dari tanaman tomat agar meringangkan beban kerja. Kelas yang dipilih dan jumlah akhir dari dataset adalah sebagai berikut:

- healthy: 2407
- Spider_mites Two-spotted_spider_mite: 2176
- Late_blight: 2314
- Tomato_Yellow_Leaf_Curl_Virus: 2451
- Septoria_leaf_spot: 2181

- Total = 11529 gambar

Menghapus semua folder kecuali folder yang akan digunakan.
"""

def delete_unwanted_folders(base_path, keep_folders=['healthy', 'Spider_mites Two-spotted_spider_mite',
                                                     'Late_blight', 'Tomato_Yellow_Leaf_Curl_Virus',
                                                     'Septoria_leaf_spot']):
    for item in os.listdir(base_path):  # Iterasi semua item di dalam folder utama
        item_path = os.path.join(base_path, item)  # Buat path lengkap ke item
        if os.path.isdir(item_path) and item not in keep_folders:  # Jika item adalah folder dan bukan yang ingin disimpan
            shutil.rmtree(item_path)  # Hapus folder beserta isinya
            print(f"Menghapus folder: {item_path}")  # Tampilkan folder yang dihapus

# Path ke folder utama yang berisi dataset
base_path = "/content/Tomato"

# Jalankan fungsi untuk menghapus folder yang tidak diinginkan
delete_unwanted_folders(base_path)

"""Membagi dataset menjadi train dan test dengan rasio 8:2."""

def split_dataset(base_path, train_ratio=0.7, val_ratio=0.15):
     # Path untuk dataset pelatihan, validasi, dan pengujian
    train_path = os.path.join(base_path, 'train')
    val_path = os.path.join(base_path, 'validation')
    test_path = os.path.join(base_path, 'test')

    # Membuat folder train, validation, dan test jika belum ada
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    for root, dirs, files in os.walk(base_path):
        if root == base_path:  # Lewati folder utama
            continue

        class_name = os.path.basename(root)  # Ambil nama kelas
        if class_name in ['train', 'validation', 'test']:  # Lewati jika sudah ada
            continue

        # Buat folder untuk kelas di dalam train, validation, dan test
        train_class_path = os.path.join(train_path, class_name)
        val_class_path = os.path.join(val_path, class_name)
        test_class_path = os.path.join(test_path, class_name)
        os.makedirs(train_class_path, exist_ok=True)
        os.makedirs(val_class_path, exist_ok=True)
        os.makedirs(test_class_path, exist_ok=True)

        # Acak urutan file sebelum dibagi
        random.shuffle(files)

        # Hitung jumlah file untuk setiap set
        total_files = len(files)
        train_split = int(train_ratio * total_files)
        val_split = int((train_ratio + val_ratio) * total_files)

        train_files = files[:train_split]
        val_files = files[train_split:val_split]
        test_files = files[val_split:]

        # Pindahkan file ke folder train
        for file in train_files:
            shutil.move(os.path.join(root, file), os.path.join(train_class_path, file))

        # Pindahkan file ke folder validation
        for file in val_files:
            shutil.move(os.path.join(root, file), os.path.join(val_class_path, file))

        # Pindahkan file ke folder test
        for file in test_files:
            shutil.move(os.path.join(root, file), os.path.join(test_class_path, file))

# Path ke folder utama yang berisi dataset
base_path = "/content/Tomato"

# Jalankan fungsi untuk membagi dataset menjadi train, validation, dan test
split_dataset(base_path)

"""Menghapus folder selain folder train,test, dan Validation"""

def delete_unwanted_folders(base_path, keep_folders=['train', 'test', 'validation']):
    for item in os.listdir(base_path):  # Iterasi semua item dalam folder utama
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item not in keep_folders:  # Hapus jika bukan folder yang dipertahankan
            shutil.rmtree(item_path)  # Hapus folder beserta isinya
            print(f"Menghapus folder: {item_path}")  # Menampilkan folder yang dihapus

# Path ke folder utama
base_path = "/content/Tomato"

# Jalankan fungsi untuk menghapus folder yang tidak diperlukan
delete_unwanted_folders(base_path)

"""## Modelling

Menggunakan ImageDataGenerator untuk melakukan augmentasi, rescale, dan mengubah target size.

Dataset test hanya akan dilakukan rescale.
"""

def augment_and_resize_dataset(base_path, img_size=(150, 150), batch_size=32):
    train_path = os.path.join(base_path, 'train')  # Path ke folder train
    val_path = os.path.join(base_path, 'validation')  # Path ke folder validation
    test_path = os.path.join(base_path, 'test')  # Path ke folder test

    # Augmentasi hanya untuk train set
    train_datagen = ImageDataGenerator(
        rescale=1./255,  # Normalisasi nilai piksel ke [0,1]
        zoom_range=0.2,  # Zooming acak hingga 20%
        horizontal_flip=True,  # Membalik gambar secara horizontal
        fill_mode='nearest'  # Mengisi piksel kosong akibat transformasi
    )

    # Hanya normalisasi untuk validasi & test set (tidak ada augmentasi)
    val_test_datagen = ImageDataGenerator(rescale=1./255)

    # Generator untuk train set
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,  # Ubah ukuran gambar ke target
        batch_size=batch_size,  # Ukuran batch dalam pelatihan
        class_mode='categorical'  # Klasifikasi multi-kelas
    )

    # Generator untuk validation set
    val_generator = val_test_datagen.flow_from_directory(
        val_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    # Generator untuk test set
    test_generator = val_test_datagen.flow_from_directory(
        test_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    return train_generator, val_generator, test_generator  # Mengembalikan 3 generator

# Path ke folder utama dataset
base_path = "/content/Tomato"

# Jalankan fungsi augmentasi dan resize dataset
train_generator, val_generator, test_generator = augment_and_resize_dataset(base_path)

"""Menampilkan kelas-kelas yang terdapat pada dataset."""

class_indices = train_generator.class_indices  # Mendapatkan indeks kelas
print(class_indices)  # Menampilkan mapping kelas ke indeks

"""Menggunakan transferlearning dari MobileNetV2. Input shape yang digunakan adalah 150x150, layers di freeze agar tidak dilatih kembali, dan menambahkan beberapa layer Conv dan Pooling."""

# Menggunakan MobileNetV2 sebagai feature extractor tanpa fully connected layer (include_top=False)
pre_trained_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(150,150,3))

# Membekukan semua layer MobileNetV2 agar tidak dilatih ulang
for layer in pre_trained_model.layers:
    layer.trainable = False

# Membuat model Sequential
model = Sequential()

# Menambahkan MobileNetV2 sebagai base model
model.add(pre_trained_model)

# Menambahkan lapisan tambahan untuk ekstraksi fitur lebih lanjut
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))  # Layer konvolusi dengan 32 filter
model.add(MaxPooling2D((2, 2)))  # Pooling untuk mengurangi dimensi fitur
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))  # Layer konvolusi dengan 64 filter
model.add(MaxPooling2D((2, 2)))  # Pooling kembali untuk mengurangi dimensi fitur

# Meratakan fitur menjadi vektor 1D
model.add(Flatten(name="flatten"))

# Dropout untuk mengurangi overfitting
model.add(Dropout(0.5))

# Fully connected layer dengan 128 unit
model.add(Dense(128, activation="relu"))

# Output layer dengan 5 unit (jumlah kelas) dan aktivasi softmax untuk klasifikasi multi-kelas
model.add(Dense(5, activation='softmax'))

"""Mengcompile model dengan optimizer Adam, loss categorical_crossentropy, dan metrics accuracy."""

# Menggunakan optimizer Adam untuk mempercepat konvergensi
optimizer = tf.optimizers.Adam()

# Kompilasi model dengan loss categorical_crossentropy (karena klasifikasi multi-kelas)
model.compile(optimizer=optimizer,
              loss='categorical_crossentropy',  # Digunakan untuk klasifikasi multi-kelas
              metrics=['accuracy'])  # Menggunakan metrik akurasi untuk evaluasi performa

"""Membuat callbacks yang memonitor val_accuracy dan akan berhenti jika tidak mengalami perubahan selama 3 epochs."""

# Menyimpan model terbaik berdasarkan nilai val_loss yang paling kecil
checkpoint = ModelCheckpoint('best_model.keras', monitor='val_loss', save_best_only=True, mode='min')

# Menghentikan pelatihan lebih awal jika val_accuracy tidak meningkat dalam 3 epoch berturut-turut
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, min_delta=0.001,
                               restore_best_weights=True, mode='max', baseline=0.96)

"""Melatih model selama 15 epoch dan menggunakan data test sebagai validation."""

num_epochs = 15  # Jumlah epoch pelatihan

"""Melatih model selama 15 epoch dan menggunakan validation set untuk evaluasi selama pelatihan."""

num_epochs = 15  # Jumlah epoch pelatihan

H = model.fit(
    train_generator,       # Data latih yang telah diaugmentasi
    epochs=num_epochs,     # Jumlah epoch yang ditentukan (15)
    validation_data=valid_generator,  # Menggunakan validation set yang benar
    verbose=1              # Menampilkan log pelatihan
)


test_loss, test_acc = model.evaluate(test_generator, verbose=1)
print(f"Test Accuracy: {test_acc:.4f}")

"""## Evaluasi dan Visualisasi

Menampilkan grafik train dan val akurasi serta train dan val loss.
"""

def plot_training_history(history):
    # Mengambil data akurasi dan loss dari hasil training
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)  # Menentukan jumlah epoch

    plt.figure(figsize=(12, 4))  # Mengatur ukuran figure

    # Plot untuk Training & Validation Accuracy
    plt.subplot(1, 2, 1)  # Membuat subplot pertama
    plt.plot(epochs, acc, 'r', label='Training acc')  # Plot akurasi training
    plt.plot(epochs, val_acc, 'b', label='Validation acc')  # Plot akurasi validasi
    plt.title('Training and validation accuracy')  # Judul plot
    plt.legend()  # Menampilkan legenda

    # Plot untuk Training & Validation Loss
    plt.subplot(1, 2, 2)  # Membuat subplot kedua
    plt.plot(epochs, loss, 'r', label='Training loss')  # Plot loss training
    plt.plot(epochs, val_loss, 'b', label='Validation loss')  # Plot loss validasi
    plt.title('Training and validation loss')  # Judul plot
    plt.legend()  # Menampilkan legenda

    plt.show()  # Menampilkan plot

# Memanggil fungsi untuk menampilkan grafik hasil training
plot_training_history(H)

"""## Konversi Model

Menyimpan model menjadi format .h5.
"""

model.save("model.h5")

"""# Konversi TFJS

Konversi model menjadi format TFJS.
"""

!tensorflowjs_converter --input_format=keras model.h5 tfjs_model

"""# Konversi SavedModel

Konversi menjadi saved_model.
"""

# Menentukan path tempat model akan disimpan
save_path = os.path.join("model/klasifikasi_gambar/1/")

# Menyimpan model dalam format TensorFlow SavedModel
tf.saved_model.save(model, save_path)  # Format ini digunakan untuk TensorFlow Serving atau deployment

"""# Konversi TF-Lite

Konversi model menjadi format TFLITE dan menyimpan label.txt.
"""

# Memuat model Keras yang telah disimpan dalam format .h5
model_TFLITE = tf.keras.models.load_model('model.h5')

# Mengonversi model ke format TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model_TFLITE)  # Membuat konverter dari model Keras
tflite_model = converter.convert()  # Mengubah model ke format TFLite

# Menyimpan model yang telah dikonversi ke dalam file .tflite
with open("converted_model.tflite", "wb") as f:
    f.write(tflite_model)  # Menyimpan model dalam bentuk biner ke file

# Buat konten yang akan ditulis ke dalam file
content = """healthy
Spider_mites Two-spotted_spider_mite
Late_blight
Tomato_Yellow_Leaf_Curl_Virus
Septoria_leaf_spot"""

# Tentukan path dan nama file untuk menyimpan label klasifikasi
file_path = "/content/model/klasifikasi_gambar.txt"

# Tulis konten ke dalam file
with open(file_path, "w") as file:
    file.write(content)  # Menulis label klasifikasi ke dalam file

# Tentukan folder yang akan dikompresi
folder_models = '/content/model'
folder_tfjs_model = '/content/tfjs_model'

# Tentukan nama file output ZIP (tanpa ekstensi .zip)
output_models = '/content/model'  # Hasilnya akan menjadi models.zip
output_tfjs_model = '/content/tfjs_model'  # Hasilnya akan menjadi tfjs_model.zip

# Mengompresi folder menjadi file ZIP
shutil.make_archive(output_models, 'zip', folder_models)  # Membuat models.zip
shutil.make_archive(output_tfjs_model, 'zip', folder_tfjs_model)  # Membuat tfjs_model.zip

!pip freeze > requirements.txt

"""## Inference (Optional)"""

