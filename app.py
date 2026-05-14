import streamlit as st
import io
from docx import Document
from PyPDF2 import PdfReader

# 1. INISIALISASI SISTEM PENYIMPANAN
if "fs" not in st.session_state:
    st.session_state.fs = {"Hukum": {"_files": {}, "_sub": {}}}
if "path" not in st.session_state:
    st.session_state.path = ["Hukum"]

# Fungsi Navigasi ke Folder Aktif
def get_curr():
    curr = st.session_state.fs
    for p in st.session_state.path:
        curr = curr[p]["_sub"]
    return curr

def get_curr_files():
    curr = st.session_state.fs
    for p in st.session_state.path:
        curr = curr[p]
    return curr["_files"]

# 2. SETUP HALAMAN
st.set_page_config(page_title="Legal Workspace AI", layout="wide")

if "auth" not in st.session_state:
    st.title("⚖️ Legal Private Workspace")
    if st.button("Masuk dengan Akun Google"):
        st.session_state.auth = True
        st.rerun()
    st.stop()

# --- SIDEBAR: NAVIGASI & STRUKTUR ---
with st.sidebar:
    st.title("📂 Explorer")
    st.write(f"📍 `{' > '.join(st.session_state.path)}` ")
    
    if len(st.session_state.path) > 1:
        if st.button("⬅️ Kembali ke Atas"):
            st.session_state.path.pop()
            st.rerun()

    st.divider()
    st.subheader("Buat Folder Baru")
    new_f_name = st.text_input("Nama Folder:")
    if st.button("Tambah Folder"):
        if new_f_name:
            get_curr()[new_f_name] = {"_files": {}, "_sub": {}}
            st.rerun()

# --- KONTEN UTAMA ---
st.title("Sistem Manajemen Dokumen Hukum")

tab1, tab2 = st.tabs(["🗂️ Pengelola Folder & File", "🔗 Koneksi & AI"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    # --- KOLOM 1: MANAJEMEN FOLDER ---
    with col1:
        st.subheader("Sub-Folder")
        folders = get_curr()
        if not folders:
            st.info("Folder kosong")
        for f_name in list(folders.keys()):
            c_a, c_b = st.columns([4, 1])
            if c_a.button(f"📁 {f_name}", use_container_width=True):
                st.session_state.path.append(f_name)
                st.rerun()
            if c_b.button("🗑️", key=f"del_f_{f_name}"):
                del folders[f_name]
                st.rerun()

    # --- KOLOM 2: MANAJEMEN FILE ---
    with col2:
        st.subheader("Dokumen di Folder Ini")
        uploaded = st.file_uploader("Tambah Dokumen (PDF/Word)", type=['pdf', 'docx', 'txt'])
        
        if uploaded:
            files = get_curr_files()
            files[uploaded.name] = {
                "content": uploaded.getvalue(),
                "type": uploaded.type
            }
            st.toast("File ditambahkan!")

        st.divider()
        files = get_curr_files()
        if not files:
            st.write("Tidak ada file.")
        for f_name in list(files.keys()):
            f_col1, f_col2, f_col3 = st.columns([3, 1, 1])
            f_col1.write(f"📄 {f_name}")
            if f_col2.button("👁️ Lihat", key=f"view_{f_name}"):
                st.session_state.viewing = files[f_name]
                st.session_state.viewing_name = f_name
            if f_col3.button("🗑️", key=f"del_f_{f_name}"):
                del files[f_name]
                st.rerun()

# --- AREA BACA DOKUMEN (PREVIEW) ---
if "viewing" in st.session_state:
    st.divider()
    st.header(f"📖 Pratinjau: {st.session_state.viewing_name}")
    v_file = st.session_state.viewing
    
    try:
        if "pdf" in v_file['type']:
            reader = PdfReader(io.BytesIO(v_file['content']))
            text = "".join([page.extract_text() for page in reader.pages])
            st.text_area("Isi PDF (Teks):", text, height=300)
        elif "word" in v_file['type'] or st.session_state.viewing_name.endswith(".docx"):
            doc = Document(io.BytesIO(v_file['content']))
            text = "\n".join([p.text for p in doc.paragraphs])
            st.text_area("Isi Dokumen Word:", text, height=300)
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")

    if st.button("Tutup Pratinjau"):
        del st.session_state.viewing
        st.rerun()

with tab2:
    st.subheader("Hubungkan Antar Kalimat/Pasal")
    st.write("Gunakan fitur ini untuk menyambungkan poin hukum.")
    source = st.text_input("Kalimat A")
    target = st.text_input("Terhubung ke B")
    if st.button("Simpan Hubungan"):
        st.success(f"Link Tersimpan: {source} → {target}")
    
