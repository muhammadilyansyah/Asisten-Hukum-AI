import streamlit as st
import io
from docx import Document
from PyPDF2 import PdfReader

# 1. SETUP LOGIKA PENYIMPANAN (Database Simulasi)
if "file_system" not in st.session_state:
    # Struktur Folder Awal
    st.session_state.file_system = {
        "Hukum": {
            "Hukum Pidana": {
                "Pidana Umum": {},
                "Pidana Khusus": {},
                "Files": [] # Tempat menyimpan file sesungguhnya
            },
            "Hukum Perdata": {
                "Files": []
            },
            "Files": []
        }
    }
if "current_path" not in st.session_state:
    st.session_state.current_path = ["Hukum"]

# 2. FUNGSI NAVIGASI FOLDER
def get_current_folder(fs, path):
    curr = fs
    for folder in path:
        curr = curr[folder]
    return curr

# 3. TAMPILAN UTAMA
st.set_page_config(page_title="Legal Folder Manager", layout="wide")

if "auth" not in st.session_state:
    st.title("⚖️ Digital Legal Archive")
    if st.button("Login dengan Google"):
        st.session_state.auth = True
        st.rerun()
    st.stop()

# --- SIDEBAR: NAVIGASI ---
with st.sidebar:
    st.header("📂 Explorer")
    if st.button("🏠 Ke Root (Awal)"):
        st.session_state.current_path = ["Hukum"]
    
    st.divider()
    st.write(f"**Lokasi Saat Ini:** \n` {' > '.join(st.session_state.current_path)} `")

# --- KONTEN UTAMA ---
st.title("📚 Manajemen Dokumen Hukum")

curr_folder = get_current_folder(st.session_state.file_system, st.session_state.current_path)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Sub-Folder")
    # Menampilkan Folder di dalam Folder aktif
    subfolders = [f for f in curr_folder.keys() if f != "Files"]
    for f in subfolders:
        if st.button(f"📁 {f}", key=f):
            st.session_state.current_path.append(f)
            st.rerun()
    
    st.divider()
    new_f = st.text_input("Buat Folder Baru:")
    if st.button("Tambah Folder"):
        if new_f and new_f not in curr_folder:
            curr_folder[new_f] = {"Files": []}
            st.success(f"Folder '{new_f}' dibuat")
            st.rerun()

with col2:
    st.subheader("Daftar Dokumen")
    # Upload File ke Folder ini
    uploaded = st.file_uploader("Upload ke folder ini", type=['pdf', 'docx', 'txt'])
    if uploaded:
        if "Files" not in curr_folder: curr_folder["Files"] = []
        # Simpan file ke dalam memori aplikasi
        file_data = {
            "name": uploaded.name,
            "type": uploaded.type,
            "content": uploaded.getvalue()
        }
        curr_folder["Files"].append(file_data)
        st.toast("File berhasil disimpan!")

    # Menampilkan File yang sudah tersimpan
    if "Files" in curr_folder and curr_folder["Files"]:
        for idx, f in enumerate(curr_folder["Files"]):
            col_f1, col_f2 = st.columns([3, 1])
            with col_f1:
                st.write(f"📄 {f['name']}")
            with col_f2:
                if st.button("Buka/Baca", key=f"btn_{idx}"):
                    st.session_state.view_file = f
    else:
        st.info("Belum ada dokumen di folder ini.")

# --- FITUR BACA DOKUMEN ---
if "view_file" in st.session_state:
    st.divider()
    st.header(f"📖 Membaca: {st.session_state.view_file['name']}")
    f = st.session_state.view_file
    
    if f['type'] == "application/pdf":
        st.warning("Pratinjau PDF: Gunakan tombol download di bawah untuk membaca lengkap.")
    elif "word" in f['type'] or f['name'].endswith(".docx"):
        doc = Document(io.BytesIO(f['content']))
        full_text = "\n".join([para.text for para in doc.paragraphs])
        st.text_area("Isi Dokumen:", full_text, height=400)
    
    st.download_button("Download File Ini", f['content'], f['name'])
    if st.button("Tutup Pratinjau"):
        del st.session_state.view_file
        st.rerun()

# --- FITUR KONEKSI (Knowledge Link) ---
st.divider()
st.subheader("🔗 Koneksi Antar Pasal")
st.caption("Contoh: Hubungkan Pasal 340 KUHP ke Putusan No. 12/2026")
c1, c2 = st.columns(2)
with c1:
    source = st.text_input("Kalimat/Pasal A")
with c2:
    target = st.text_input("Terkoneksi ke Dokumen B")
if st.button("Buat Tautan"):
    st.success(f"Tautan Tercipta: {source} <---> {target}")
    
