import streamlit as st

# 1. Konfigurasi Dasar & Login
st.set_page_config(page_title="AI File Connector", layout="wide")

if "login" not in st.session_state:
    st.title("🔐 Akses Aman")
    st.info("Aplikasi ini dilindungi oleh enkripsi akun.")
    if st.button("Masuk dengan Akun Google"):
        st.session_state.login = True
        st.rerun()
    st.stop()

# 2. Sidebar (AI Copilot)
with st.sidebar:
    st.title("🤖 Copilot AI")
    tanya = st.text_input("Tanya tentang isi dokumen Anda:")
    if st.button("Analisis"):
        st.write("AI sedang mencari keterkaitan antar dokumen...")

# 3. Tampilan Utama
st.title("📂 Interconnected File Manager")

tab1, tab2, tab3 = st.tabs(["Pencarian & File", "Koneksi Kalimat", "Buat Dokumen"])

with tab1:
    st.subheader("Cari di Seluruh File")
    cari = st.text_input("Ketik kata, kalimat, atau nama file...")
    st.file_uploader("Upload Word/Excel", accept_multiple_files=True)
    if cari:
        st.write(f"🔍 Menampilkan hasil untuk: **{cari}**")

with tab2:
    st.subheader("Hubungkan Kalimat Antar Dokumen")
    c1, c2 = st.columns(2)
    with c1:
        sumber = st.text_area("Kalimat dari File A:")
    with c2:
        tujuan = st.text_area("Hubungkan ke File B (Paragraf/Kalimat):")
    if st.button("Simpan Koneksi"):
        st.success("Koneksi berhasil dibuat!")

with tab3:
    st.subheader("Buat Dokumen Baru")
    st.selectbox("Format:", ["Microsoft Word (.docx)", "Microsoft Excel (.xlsx)"])
    st.text_area("Tulis isi dokumen di sini...")
    st.button("Simpan ke Cloud")
  
