import json
import os

def process_notebook(filepath, fix_funcs):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell["source"])
            new_source = source
            for func in fix_funcs:
                new_source = func(new_source)
            if new_source != source:
                # Need to convert back to list of strings with newlines
                # Simplest way is to split by \n and append \n, except the last
                lines = new_source.split('\n')
                cell["source"] = [line + '\n' for line in lines[:-1]] + [lines[-1]] if lines else []

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

# ---- Fixes for NB 01 ----
def fix_nb01(source):
    # 1. Header/Footer
    source = source.replace(
        "r'Disclaimer[\\s\\S]{0,200}?digunakan',",
        "r'Disclaimer[\\s\\S]*?telp\\s*:\\s*021[\\-\\d\\s(ext.)]+',\n    r'hal\\.\\s*put\\.\\s*nomor\\s*\\d+\\s*k/pid/\\d{4}',\n    r'halaman\\s+\\d+',"
    )
    # 2. Validation
    val_old = "    is_valid = content_ok and keyword_ok"
    val_new = (
        "    REQUIRED_SECTIONS = ['dakwaan', 'menimbang', 'mengadili', 'memutuskan']\n"
        "    sections_found = sum(1 for s in REQUIRED_SECTIONS if s in text.lower())\n"
        "    structure_ok = sections_found >= 3\n"
        "    is_valid = content_ok and keyword_ok and structure_ok"
    )
    source = source.replace(val_old, val_new)
    return source

# ---- Fixes for NB 02 ----
def fix_nb02(source):
    # 1. no_perkara
    if "def extract_no_perkara" in source:
        source = source.replace(
            "r'(\\d+/pid\\.b/\\d{4}/pn\\.?[a-z]+)',",
            "r'nomor\\s+(\\d+\\s*k\\s*/\\s*pid(?:\\.sus|\\.b)?\\s*/\\s*\\d{4})',\n        r'nomor\\s+(\\d+\\s*pk\\s*/\\s*pid\\s*/\\s*\\d{4})',\n        r'(\\d+/pid\\.b/\\d{4}/pn\\.?[a-z]+)',"
        )
    # 2. tanggal
    if "def extract_tanggal" in source:
        source = source.replace(
            "r'(\\d{1,2})\\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\\s+(\\d{4})',",
            "r'diucapkan.*?tanggal\\s+(\\d{1,2})\\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\\s+(\\d{4})',\n        r'(?:demikianlah|diputuskan).*?tanggal\\s+(\\d{1,2})\\s+(\\w+)\\s+(\\d{4})',\n        r'(\\d{1,2})\\s+(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\\s+(\\d{4})',"
        )
    # 3. pihak
    if "def extract_pihak" in source:
        source = source.replace(
            "r'terdakwa[\\s:]+([A-Z][A-Z\\s]+?)(?:\\s+(?:bin|binti|alias|als|,|;))',",
            "r'(?:terdakwa|nama lengkap)\\s*[:\\s]+([a-z][a-z\\s,.]{3,50}?)(?:\\s*;|\\n|,\\s*(?:alias|bin|binti))',\n        r'terdakwa[\\s:]+([A-Z][A-Z\\s]+?)(?:\\s+(?:bin|binti|alias|als|,|;))',"
        )
    # 4. vonis
    if "def extract_vonis" in source:
        source = source.replace(
            "r'(?:pidana penjara|hukuman penjara)[\\s]*(?:selama)?[\\s]*(\\d+[\\s]*(?:tahun|bulan|hari)[\\s\\w]*)',",
            "r'(?:menjatuhkan pidana|dipidana)\\s+(?:penjara\\s+)?(?:selama\\s+)?(\\d+(?:\\s*\\(\\w+\\)\\s*)?\\s*(?:tahun|bulan)(?:\\s+dan\\s+\\d+\\s*(?:bulan|hari))?)',\n        r'pidana\\s+penjara\\s+selama\\s+(\\d+\\s*(?:\\(\\w+\\)\\s*)?\\s*(?:tahun|bulan)(?:\\s+dan\\s+\\d+\\s*(?:\\(\\w+\\)\\s*)?\\s*(?:bulan|hari))?)',\n        r'(?:pidana penjara|hukuman penjara)[\\s]*(?:selama)?[\\s]*(\\d+[\\s]*(?:tahun|bulan|hari)[\\s\\w]*)',"
        )
    return source

# ---- Fixes for NB 03 ----
def fix_nb03(source):
    # ground truth
    old_gt = """similar_train = df_train[
        df_train["pasal"].str.contains(
            pasal_query[:10] if pasal_query != "TIDAK_DITEMUKAN" else "000",
            na=False, regex=False
        )
    ]["case_id"].tolist()"""
    
    new_gt = """pasal_set = set([p.strip() for p in pasal_query.split(',') if p.strip()])
    def is_similar(p_train):
        if not p_train or p_train == "TIDAK_DITEMUKAN": return False
        pt_set = set([p.strip() for p in p_train.split(',') if p.strip()])
        return len(pasal_set.intersection(pt_set)) > 0
        
    similar_train = df_train[df_train["pasal"].apply(is_similar)]["case_id"].tolist() if pasal_query != "TIDAK_DITEMUKAN" else []"""
    
    source = source.replace(old_gt, new_gt)
    return source

# ---- Fixes for NB 04 & 05 ----
def fix_nb04_05(source):
    # normalize_vonis
    old_nv = 'if not vonis_text or vonis_text == "TIDAK_DITEMUKAN":'
    new_nv = 'if not vonis_text or vonis_text in ("TIDAK_DITEMUKAN", "TIDAK_DIKETAHUI"):'
    source = source.replace(old_nv, new_nv)
    return source

# --- RUN ---
base_path = r"c:\Semester 6\PENALARAN KOMPUTER\cbr_project-main\cbr_project-main\notebooks"

process_notebook(os.path.join(base_path, "01_case_base.ipynb"), [fix_nb01])
process_notebook(os.path.join(base_path, "02_case_representation.ipynb"), [fix_nb02])
process_notebook(os.path.join(base_path, "03_case_retrieval.ipynb"), [fix_nb03])
process_notebook(os.path.join(base_path, "04_solution_reuse.ipynb"), [fix_nb04_05])
process_notebook(os.path.join(base_path, "05_evaluation.ipynb"), [fix_nb04_05])

print("Done fixing notebooks!")
