# Ringkasan Perbaikan QA/QC (Quality Assurance & Quality Control)

Dokumen ini merangkum seluruh perbaikan bug, penyesuaian logika, dan pembenahan arsitektur yang dilakukan pada source code Jupyter Notebooks (01 - 05) dalam proyek Case-Based Reasoning (CBR) Putusan Pengadilan ini.

## 1. Pembersihan Teks (Notebook 01)
*   **Bug Sebelumnya:** Teks *Disclaimer* Mahkamah Agung gagal dihapus dengan sempurna karena regex membatasi rentang karakter terlalu pendek (hanya 200 karakter). Hal ini menyebabkan dokumen kotor dengan kata "informasi", "kepaniteraan", dan "mahkamah".
*   **Perbaikan:** Regex pencarian *header* dan *footer* diperluas. Ditambahkan pola spesifik untuk menangkap blok *disclaimer* Mahkamah Agung, teks "hal. put. nomor...", dan "halaman ...".

## 2. Validasi Keutuhan Dokumen (Notebook 01)
*   **Bug Sebelumnya:** Validasi dokumen PDF hanya mengecek jumlah kata dan rasio kata kunci acak, sehingga dokumen yang terpotong secara struktural masih dianggap utuh.
*   **Perbaikan:** Ditambahkan pengecekan struktural secara eksplisit. Dokumen baru dianggap valid jika memuat setidaknya 3 dari 4 bagian krusial putusan hukum: `['dakwaan', 'menimbang', 'mengadili', 'memutuskan']`.

## 3. Ekstraksi Nomor Perkara (Notebook 02)
*   **Bug Sebelumnya:** Logika regex memprioritaskan pengambilan nomor perkara Pengadilan Negeri (PN), sehingga nomor perkara Mahkamah Agung (Kasasi) tertimpa dan gagal diekstrak.
*   **Perbaikan:** Pola regex diubah urutannya. Prioritas tertinggi kini diberikan untuk mencari pola nomor perkara Mahkamah Agung (K/PID/...).

## 4. Ekstraksi Tanggal Putusan (Notebook 02)
*   **Bug Sebelumnya:** Regex hanya mencari keberadaan pola *tanggal pertama* yang ada di dalam putusan. Seringkali, ini menyebabkan sistem justru mengekstrak "Tanggal Lahir Terdakwa".
*   **Perbaikan:** Regex dipersempit konteksnya hanya untuk menangkap pola tanggal yang diawali dengan kata pengantar vonis seperti `"diucapkan... tanggal"`, `"demikianlah... tanggal"`, atau `"diputuskan... tanggal"`.

## 5. Ekstraksi Pihak Terdakwa (Notebook 02)
*   **Bug Sebelumnya:** Regex mencari teks dengan huruf besar kapital `[A-Z]`. Karena keseluruhan teks PDF sudah diturunkan menjadi *lowercase* di Notebook 01, pola ini gagal 100% dan jatuh ke pencarian *fallback* yang seringkali asal.
*   **Perbaikan:** Regex disesuaikan agar mampu membedah format *lowercase* (`[a-z]`) untuk blok `"terdakwa"` maupun `"nama lengkap"`. Hasil ekstraksi terdakwa meningkat dari 30/35 menjadi 35/35 (100%).

## 6. Ekstraksi Vonis Hukuman (Notebook 02)
*   **Bug Sebelumnya:** Pola pencarian vonis terlalu kaku dan hanya berfokus pada format frasa pengadilan tingkat pertama (`"pidana penjara selama X tahun"`). Hanya 17% (6/35) vonis yang berhasil diekstrak.
*   **Perbaikan:** Pola regex vonis diperluas untuk mengakomodir gaya penulisan kasasi dan bahasa hukum MA. Keberhasilan ekstraksi vonis melonjak dari 17% menjadi 80% (28/35).

## 7. Pencarian *Ground Truth* Retrieval (Notebook 03)
*   **Bug Sebelumnya:** Metode validasi mencari kasus relevan (*ground truth*) di data latih hanya dengan memotong 10 karakter pertama dari string Pasal. Akibatnya, validasi buta terhadap keseluruhan pasal yang tumpang tindih.
*   **Perbaikan:** Logika pencarian diubah menggunakan **Set Intersection** (irisan himpunan). Sistem kini memecah seluruh pasal menjadi array tunggal dan mencari kecocokan setidaknya 1 pasal krusial yang saling tumpang tindih antar kasus.

## 8. Koreksi Akurasi Evaluasi Palsu (Notebook 04 & 05)
*   **Bug Sebelumnya:** Fungsi `normalize_vonis()` tidak mengenal flag `"TIDAK_DIKETAHUI"`, sehingga kasus yang vonisnya gagal diekstrak diubah paksa menjadi kategori `"PENJARA_LAIN"`. Hal ini membuat perhitungan metrik Accuracy dan F1-Score membesar tanpa dasar (menghasilkan angka ilusi akurasi 71.43%).
*   **Perbaikan:** Ditambahkan pengecekan eksplisit agar `TIDAK_DIKETAHUI` dilewati dan ditangani secara objektif. Dengan ekstraksi vonis yang telah diperbaiki pada poin 6, akurasi prediksi kini terukur pada angka **85.71%**, sebuah peningkatan valid berdasarkan kapabilitas sistem CBR yang sesungguhnya.
