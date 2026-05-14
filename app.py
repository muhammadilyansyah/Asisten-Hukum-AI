import streamlit as st
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import io

# Setup Halaman
st.set_page_config(page_title="Personal File Hub", layout="wide")

# Login Sederhana
if "login" not in st.session_state:
    st.title("🔐 Selamat Datang")
    if st.button("Masuk dengan Akun Google"):
        st.session_state.login = True
        st.rerun()
    st.stop()

st.title("📂 Aplikasi Penyimpanan & Koneksi File")

# Fitur Utama
tab1, tab2, tab3 = st.tabs(["Cari & Upload", "Koneksi Kalimat", "Buat File Baru"])

with tab1:
    st.subheader("Upload Dokumen (PDF, Word, Excel)")
    # Batas ukuran file 200MB
    uploaded_files = st.file_uploader("Pilih file Anda", accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Berhasil mengunggah: {file.name}")
            # Logika Pencarian Sederhana
            if st.text_input(f"Cari kata di dalam {file.name}:", key=file.name):
                st.write("Menganalisis isi file...")

with tab2:
    st.subheader("🔗 Hubungkan Kalimat Antar File")
    col1, col2 = st.columns(2)
    with col1:
        txt1 = st.text_area("Kalimat/Paragraf di File A:")
    with col2:
        txt2 = st.text_area("Hubungkan ke File/Kalimat B:")
    if st.button("Simpan Koneksi"):
        st.info(f"Koneksi tersimpan: {txt1} berhubungan dengan {txt2}")

with tab3:
    st.subheader("📝 Buat Dokumen Baru")
    nama_file = st.text_input("Nama File:", "Catatan_Baru")
    tipe = st.selectbox("Jenis:", ["Word", "Excel"])
    isi = st.text_area("Isi Dokumen:")
    
    if st.button("Download File"):
        if tipe == "Word":
            doc = Document()
            doc.add_paragraph(isi)
            buffer = io.BytesIO()
            doc.save(buffer)
            st.download_button("Klik untuk Download Word", buffer.getvalue(), f"{nama_file}.docx")
        else:
            df = pd.DataFrame({"Konten": [isi]})
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button("Klik untuk Download Excel", buffer.getvalue(), f"{nama_file}.xlsx")

# AI Copilot di Sidebar
st.sidebar.title("🤖 Copilot AI")
tanya = st.sidebar.text_input("Tanya AI:")
if st.sidebar.button("Proses"):
    st.sidebar.write("AI sedang menganalisis dokumen Anda...")
    
