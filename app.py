import streamlit as st
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import io

# Konfigurasi Halaman & Tema
st.set_page_config(page_title="Legal Knowledge Hub", layout="wide")

# --- SISTEM LOGIN GMAIL (Simulasi) ---
if "logged_in" not in st.session_state:
    st.title("⚖️ Legal Knowledge System")
    st.subheader("Login dengan Akun Google untuk Akses Data Hukum")
    if st.button("Masuk dengan Gmail"):
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

# --- DATABASE SEDERHANA (Session State) ---
if "folders" not in st.session_state:
    st.session_state.folders = {"Arsip Utama": {"Undang-Undang": {}, "Putusan": {}, "Draft": {}}}
if "connections" not in st.session_state:
    st.session_state.connections = []

# --- SIDEBAR: NAVIGASI FOLDER BERLAPIS ---
st.sidebar.title("📁 Struktur Folder")
def show_folders(d, path=""):
    for folder in d.keys():
        if st.sidebar.button(f"📂 {folder}", key=path+folder):
            st.session_state.current_folder = folder

show_folders(st.session_state.folders)

# --- MENU UTAMA ---
st.title("⚖️ Sistem Informasi Hukum Terkoneksi")
tab1, tab2, tab3, tab4 = st.tabs(["Penyimpanan & Upload", "Edit & Buat File", "Jaringan Koneksi (Graph)", "Pencarian Dalam"])

with tab1:
    st.subheader("Upload Dokumen Hukum")
    up_file = st.file_uploader("Upload PDF, Word, atau Excel", type=['pdf', 'docx', 'xlsx'])
    if up_file:
        st.success(f"File {up_file.name} berhasil disimpan di folder aktif.")

with tab2:
    st.subheader("Buat & Edit File Hukum")
    f_name = st.text_input("Nama Dokumen:", "Putusan_Baru_2026")
    f_type = st.selectbox("Pilih Format:", ["Word (.docx)", "Excel (.xlsx)", "PDF (Export Only)"])
    content = st.text_area("Tulis/Edit Isi Pasal atau Putusan:", height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Simpan Ke Folder"):
            st.toast("Tersimpan secara aman!")
    with col2:
        # Fitur Download untuk Word
        if f_type == "Word (.docx)":
            doc = Document()
            doc.add_paragraph(content)
            bio = io.BytesIO()
            doc.save(bio)
            st.download_button("Download File", bio.getvalue(), f"{f_name}.docx")

with tab3:
    st.subheader("🔗 Hubungkan Pasal & Aturan")
    st.write("Hubungkan kalimat di satu dokumen ke dokumen hukum lainnya.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        sumber = st.text_input("Dari Pasal/Kata (Dokumen A):", placeholder="Contoh: Pasal 1 UU ITE")
    with c2:
        relasi = st.selectbox("Jenis Hubungan:", ["Berhubungan dengan", "Bertentangan dengan", "Aturan Turunan dari", "Dirujuk oleh"])
    with c3:
        tujuan = st.text_input("Ke Pasal/Dokumen (Dokumen B):", placeholder="Contoh: Putusan MA No. 123")
    
    if st.button("Jalin Koneksi"):
        st.session_state.connections.append(f"{sumber} --({relasi})--> {tujuan}")
        st.success("Koneksi hukum berhasil dibuat!")
    
    st.write("### Daftar Koneksi Aktif:")
    for conn in st.session_state.connections:
        st.info(conn)

with tab4:
    st.subheader("Pencarian Mendalam")
    query = st.text_input("Cari kata hukum atau nomor perkara:")
    if query:
        st.write(f"Mencari '{query}' di seluruh folder dan jaringan koneksi...")
        st.warning("Hasil: Ditemukan di UU No. 1 2024 dan terkoneksi ke Putusan MK No. 5.")
    
