# Panduan Membaca Struktur Kode Proyek CBR

Selamat datang di repositori proyek *Case-Based Reasoning (CBR)* untuk analisis Putusan Pengadilan Pidana Umum (Pemalsuan). Agar tidak bingung, berikut adalah panduan fungsi dari masing-masing folder dan file yang ada di proyek ini:

## 📂 Struktur Utama
Secara garis besar, repositori ini dibagi menjadi **3 folder utama**:
1. `notebooks/` $\rightarrow$ Berisi otak utama program (Jupyter Notebooks).
2. `data/` $\rightarrow$ Berisi *database* kasus dari awal (PDF) hingga akhir (Hasil Evaluasi).
3. `docs/` $\rightarrow$ Berisi dokumentasi seperti perbaikan *bug*.

---

### 1. `notebooks/` (Otak Sistem / Source Code)
Jika Anda ingin melihat atau menguji logika program, buka *notebook* di folder ini secara berurutan:
*   `01_case_base.ipynb` $\rightarrow$ Mengubah file PDF menjadi teks (`.txt`) dan membersihkan bagian *header/footer/disclaimer* yang tidak penting.
*   `02_case_representation.ipynb` $\rightarrow$ Mengekstrak *metadata* (No Perkara, Tanggal, Pasal, Terdakwa, Vonis) dan menghitung *word count*. Data akhir disimpan dalam bentuk CSV.
*   `03_case_retrieval.ipynb` $\rightarrow$ Mengubah teks menjadi angka (*vector embeddings*) menggunakan model bahasa IndoBERT dan menghitung *cosine similarity* untuk mencari kasus paling mirip.
*   `04_solution_reuse.ipynb` $\rightarrow$ Memprediksi solusi (vonis hukuman) untuk sebuah kasus uji berdasarkan bobot kasus-kasus lama terdekatnya.
*   `05_evaluation.ipynb` $\rightarrow$ Menghitung angka performa (*Precision, Recall, F1-Score, MRR, Accuracy*) dan membuat visualisasi plot *chart*.

### 2. `data/` (Pusat Database)
Semua output dari proses *notebook* masuk ke sini, terbagi atas beberapa sub-folder:
*   `data/pdf_input/` $\rightarrow$ Tempat Anda menyimpan dokumen PDF asli dari Mahkamah Agung.
*   `data/raw/` $\rightarrow$ Hasil ekstrak teks kasar (`.txt`) dari PDF. Ada juga `case_mapping.json` agar *case_001* bisa dilacak berasal dari PDF yang mana.
*   `data/processed/` $\rightarrow$ Berisi `cases.csv` dan `cases.json` yang berisi data rapi yang siap dibaca tabel (termasuk isi dakwaan, pasal, dan terdakwa).
*   `data/eval/` $\rightarrow$ Data simulasi ujian (Test Set). Di sini tersimpan *embeddings* IndoBERT (`.npy`) agar tidak harus di-*run* berulang-ulang, `queries.json` sebagai kasus simulasi baru, dan tabel skor `_metrics.csv`.
*   `data/results/` $\rightarrow$ Berisi `predictions.csv` hasil dari tebakan/prediksi sistem pada tahap 4.

### 3. `docs/` dan `logs/`
*   `docs/` $\rightarrow$ Tempat saya menaruh catatan seperti `LIST_PERBAIKAN_QA_QC.md` yang merangkum *error* apa saja yang pernah ada dan bagaimana penyelesaiannya.
*   `logs/` $\rightarrow$ Laporan internal jika ada PDF yang rusak atau gagal ter-ekstrak saat tahap 1 (`validation_report.csv`).

### 4. File-file Pendukung di Luar (Root)
*   `run_all.bat` $\rightarrow$ *Script* ajaib jika Anda ingin mengeksekusi ulang seluruh *notebook* 01-05 secara otomatis dalam sekali klik/jalan (tanpa buka aplikasi Jupyter).
*   `fix_nb.py` $\rightarrow$ *Script* Python yang sebelumnya saya gunakan untuk membersihkan *bug* di dalam *notebook* Anda.
*   `generate_artikel_docx.py` & `generate_presentasi_pptx.py` $\rightarrow$ Program untuk mengubah semua hasil evaluasi kita langsung menjadi dokumen Word dan PowerPoint yang cantik.

---
**Tip:** Jika dosen Anda bertanya *"Di mana letak file ekstraksi pasal dan terdakwa?"*, Anda cukup membuka folder `data/processed/cases.csv`! Jika dosen bertanya *"Di mana kodenya?"*, arahkan ke `notebooks/02_case_representation.ipynb`.
