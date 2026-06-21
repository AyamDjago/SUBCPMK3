# Sistem Case-Based Reasoning (CBR) — Pidana Umum: Pemalsuan

> **Mata Kuliah:** Penalaran Komputer — Semester Genap 2025/2026  
> **Universitas Muhammadiyah Malang, Fakultas Teknik — Informatika**  
> **Domain Perkara:** Pidana Umum - Pemalsuan (Pasal 263–276 KUHP)  
> **Sumber Data:** [Direktori Putusan Mahkamah Agung RI](https://putusan3.mahkamahagung.go.id/)

---

## Deskripsi Proyek

Sistem ini mengimplementasikan siklus **Case-Based Reasoning (CBR)** berbasis Python untuk mendukung analisis putusan pengadilan pidana pemalsuan. Diberikan kasus baru (query berupa fakta/dakwaan), sistem menemukan kasus-kasus lama yang paling mirip dan menggunakan amar putusannya sebagai referensi solusi.

### Siklus CBR yang Diimplementasikan

```
[Kasus Baru] → Retrieve → [Top-K Mirip] → Reuse → [Prediksi Solusi] → Evaluate
                 ↑
           IndoBERT Embedding
           + Cosine Similarity
```

| Tahap | Notebook | Deskripsi |
|-------|----------|-----------|
| 1 | `01_case_base.ipynb` | Konversi PDF → teks bersih (preprocessing) |
| 2 | `02_case_representation.ipynb` | Ekstraksi metadata & fitur terstruktur |
| 3 | `03_retrieval.ipynb` | Embedding IndoBERT + fungsi `retrieve()` (alias `03_case_retrieval.ipynb`) |
| 4 | `04_predict.ipynb` | Prediksi solusi dengan weighted similarity (alias `04_solution_reuse.ipynb`) |
| 5 | `05_evaluation.ipynb` | Evaluasi Precision, Recall, F1, MRR |

---

## Struktur Repository

```
cbr_pemalsuan/
│
├── data/
│   ├── pdf_input/                    # ← LETAKKAN 35 FILE PDF DI SINI
│   ├── raw/                    # Output: teks bersih (*.txt)
│   ├── processed/
│   │   ├── cases.csv           # Representasi terstruktur (dengan text_full & pihak)
│   │   ├── cases.json          # Lengkap dengan text_full & pihak
│   │   └── solutions.json      # {case_id: amar_putusan}
│   ├── eval/
│   │   ├── train_embeddings.npy
│   │   ├── train_case_ids.json
│   │   ├── data_split.json
│   │   ├── queries.json
│   │   ├── retrieval_metrics.csv
│   │   └── prediction_metrics.csv
│   └── results/
│       └── predictions.csv
│
├── notebooks/
│   ├── 01_case_base.ipynb
│   ├── 02_case_representation.ipynb
│   ├── 03_retrieval.ipynb          # Sesuai Rubrik
│   ├── 04_predict.ipynb            # Sesuai Rubrik
│   └── 05_evaluation.ipynb
│
├── logs/
│   ├── cleaning.log
│   └── validation_report.csv
│
├── requirements.txt
├── README.md
├── LICENSE
├── artikel_cbr.docx           # Artikel ilmiah (format JOIV)
└── presentasi_cbr.pptx        # Presentasi 5 slide
```

---

## Cara Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/cbr-pemalsuan.git
cd cbr-pemalsuan
```

### 2. Buat Virtual Environment (direkomendasikan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Catatan GPU:** Jika memiliki GPU NVIDIA, install PyTorch versi CUDA untuk mempercepat proses embedding IndoBERT:
> ```bash
> # Contoh CUDA 11.8
> pip install torch --index-url https://download.pytorch.org/whl/cu118
> ```
> Tanpa GPU, proses embedding ~35 dokumen membutuhkan waktu sekitar 5–15 menit (CPU).

---

## Cara Menjalankan Pipeline End-to-End

### Langkah 0 — Siapkan Data PDF

Letakkan **35 file PDF** putusan pidana pemalsuan dari MA RI ke dalam folder:

```
data/pdf_input/
├── putusan_001.pdf
├── putusan_002.pdf
└── ... (minimal 30 file)
```

### Langkah 1 — Jalankan Jupyter Notebook

```bash
jupyter notebook
```

Kemudian jalankan notebook secara berurutan:

#### Tahap 1: Membangun Case Base
```
notebooks/01_case_base.ipynb
```
- Konversi PDF → plain text
- Pembersihan header/footer/watermark
- Validasi kelengkapan teks
- Output: `data/raw/case_001.txt` ... `case_035.txt`

#### Tahap 2: Case Representation
```
notebooks/02_case_representation.ipynb
```
- Ekstrak nomor perkara, tanggal, pasal, terdakwa
- Ekstrak dakwaan, amar putusan, vonis
- Output: `data/processed/cases.csv` dan `cases.json`

#### Tahap 3: Case Retrieval (IndoBERT)
```
notebooks/03_retrieval.ipynb
```
- Download model `indobenchmark/indobert-base-p1` (otomatis ~450MB)
- Buat embedding untuk semua kasus train
- Splitting data 80:20
- Output: `data/eval/train_embeddings.npy`

#### Tahap 4: Solution Reuse (Prediksi)
```
notebooks/04_predict.ipynb
```
- Prediksi amar putusan dengan weighted similarity
- Demo 5 kasus test
- Output: `data/results/predictions.csv`

#### Tahap 5: Evaluasi
```
notebooks/05_evaluation.ipynb
```
- Hitung Precision@K, Recall@K, F1@K, MRR
- Hitung Accuracy, Precision, Recall, F1 prediksi
- Output: `data/eval/retrieval_metrics.csv`, `prediction_metrics.csv`

---

## Contoh Penggunaan Fungsi Retrieve

Setelah menjalankan Tahap 3, Anda dapat langsung menggunakan fungsi retrieval:

```python
# Jalankan di notebook 03 atau 04 setelah semua setup selesai
query = """
terdakwa terbukti memalsukan surat keterangan domisili 
menggunakan stempel palsu untuk mengurus administrasi perbankan.
didakwa pasal 263 kuhp.
"""

# Retrieve 5 kasus paling mirip
results = retrieve(query, k=5, return_details=True)

for r in results:
    print(f"Case: {r['case_id']} | Sim: {r['similarity']:.4f} | Vonis: {r['vonis']}")
```

```python
# Prediksi solusi (amar putusan)
prediction = predict_outcome(query, k=5, method="weighted")
print("Prediksi Vonis   :", prediction["predicted_vonis"])
print("Prediksi Amar    :", prediction["predicted_solution"])
print("Referensi Cases  :", prediction["top_k_case_ids"])
```

---

## Teknis Model

| Komponen | Detail |
|----------|--------|
| Model Embedding | `indobenchmark/indobert-base-p1` |
| Pooling Strategy | Mean Pooling + L2 Normalization |
| Similarity Metric | Cosine Similarity |
| Max Token Length | 512 token |
| Split Ratio | 80% Train / 20% Test |
| Prediksi Metode | Weighted Similarity (bobot = skor cosine) |
| Fallback Metode | Majority Vote |

---

## Catatan Penting

1. **Kolom `query_text` di Tahap 3 & 4:** Teks query dibangun dari gabungan kolom `dakwaan` dan `ringkasan_fakta` menggunakan:
   ```python
   query_text = f"{row.get('dakwaan', '')} {row.get('ringkasan_fakta', '')}".strip()
   ```
   Ini lebih andal daripada kolom `embedding_text` yang hanya ada sementara di memori.

2. **Kualitas Ekstraksi:** Regex ekstraksi metadata disesuaikan untuk pola umum putusan MA RI. Jika ada putusan dengan format berbeda, nilai `TIDAK_DITEMUKAN` akan muncul — tidak mempengaruhi proses embedding.

3. **Pertama Kali Download IndoBERT:** Model akan diunduh otomatis dari Hugging Face (~450MB). Pastikan koneksi internet tersedia saat menjalankan Tahap 3 untuk pertama kali.

4. **Minimum Data:** Sistem membutuhkan minimal 30 dokumen agar split 80:20 menghasilkan data test yang representatif.

---

## Referensi

- Aamodt, A. & Plaza, E. (1994). Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches. *AI Communications*, 7(1), 39–59.
- Wilie, B. et al. (2020). IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding. *AACL-IJCNLP 2020*.
- Model IndoBERT: [indobenchmark/indobert-base-p1](https://huggingface.co/indobenchmark/indobert-base-p1)
- Direktori Putusan MA RI: [putusan3.mahkamahagung.go.id](https://putusan3.mahkamahagung.go.id/)
