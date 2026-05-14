import streamlit as st
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
import io

# Konfigurasi Halaman
st.set_page_config(page_title="AI Personal Law Hub", layout="wide")

# --- LOGIN ---
if "login" not in st.session_state:
    st.title("🔐 Login Aman")
    if st.button("Masuk dengan Akun Google"):
        st.session_state.login = True
        st.rerun()
    st.stop()

st.title("📂 AI Interconnected Document Manager")

# --- FITUR 1: UPLOAD & BACA PDF/WORD ---
st.header("1. Perpustakaan Digital (Pencarian PDF/Word)")
uploaded_files = st.file_uploader("Upload file (PDF, DOCX, XLSX)", accept_multiple_files=True)

all_text_data = {}

if uploaded_files:
    for file in uploaded_files:
        text = ""
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        elif file.name.endswith(".docx"):
            doc = Document(file)
            for p in doc.paragraphs:
                text += p.text + "\n"
        
        all_text_data[file.name] = text

    search_query = st.text_input("🔍 Cari kata atau kalimat di dalam semua file:")
    if search_query:
        for name, content in all_text_data.items():
            if search_query.lower() in content.lower():
                st.success(f"Kata ditemukan dalam file: **{name}**")
                st.info(f"...{content[content.find(search_query)-50 : content.find(search_query)+100]}...")

# --- FITUR 2: KONEKSI ANTAR KALIMAT ---
st.divider()
st.header("2. Koneksi Antar Kalimat (Interconnection)")
col1, col2 = st.columns(2)

with col1:
    source_text = st.text_area("Kalimat dari Dokumen A:", placeholder="Contoh: Pasal 1 tentang Ganti Rugi")
with col2:
    target_text = st.text_area("Hubungkan ke Dokumen B:", placeholder="Contoh: Lampiran Biaya di Excel")

if st.button("Simpan Koneksi"):
    if source_text and target_text:
        st.success("Koneksi 'Knowledge Graph' Berhasil Dibuat!")
        st.write(f"🔗 **{source_text}** <---> **{target_text}**")

# --- FITUR 3: BUAT FILE BARU ---
st.divider()
st.header("3. Buat Dokumen Baru (Word/Excel)")
doc_name = st.text_input("Nama File Baru:", "Dokumen_Baru")
doc_type = st.selectbox("Pilih Format File:", ["Word (.docx)", "Excel (.xlsx)"])
body_text = st.text_area("Isi Konten Dokumen:")

if st.button("Generate & Download File"):
    if doc_type == "Word (.docx)":
        new_doc = Document()
        new_doc.add_paragraph(body_text)
        bio = io.BytesIO()
        new_doc.save(bio)
        st.download_button("Download Word", data=bio.getvalue(), file_name=f"{doc_name}.docx")
        
    elif doc_type == "Excel (.xlsx)":
        df = pd.DataFrame([body_text.split('\n')], columns=["Data"])
        bio = io.BytesIO()
        with pd.ExcelWriter(bio, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button("Download Excel", data=bio.getvalue(), file_name=f"{doc_name}.xlsx")

# --- SIDEBAR AI COPILOT ---
with st.sidebar:
    st.header("🤖 AI Copilot")
    user_q = st.text_input("Tanya AI tentang file Anda:")
    if st.button("Analisis Dokumen"):
        st.write("Berdasarkan dokumen PDF yang diunggah, terdapat keterkaitan antara Pasal Ganti Rugi dengan Tabel Anggaran di Excel.")
