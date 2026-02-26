import google.generativeai as genai
import streamlit as st
import time

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Chatbot Ilmu Tajwid",
    page_icon="🕌",
    layout="centered"
)

# ============================================
# JUDUL DAN DESKRIPSI
# ============================================
st.title("🕌 Chatbot Ilmu Tajwid")
st.markdown("---")

st.markdown("""
Assalamu'alaikum! 👋 Saya adalah chatbot khusus yang akan membantu Anda 
belajar **Ilmu Tajwid** (hukum bacaan Al-Qur'an).

**Topik yang bisa ditanyakan:**
- ✅ Hukum Nun Mati/Tanwin (Izhar, Idgham, Iqlab, Ikhfa)
- ✅ Hukum Mim Mati (Ikhfa Syafawi, Idgham Mimi, Izhar Syafawi)
- ✅ Hukum Mad (Panjang pendek: Mad Thabi'i, Mad Wajib, Mad Jaiz, dll)
- ✅ Qalqalah dan Ghunnah
- ✅ Makhraj dan Sifat Huruf
- ✅ Tanda Waqaf
""")

st.markdown("---")

# ============================================
# SIDEBAR (INPUT API KEY)
# ============================================
with st.sidebar:
    st.header("🔑 Pengaturan")
    
    # Input API Key
    api_key = st.text_input(
        "Masukkan API Key Gemini Anda:",
        type="password",
        help="Dapatkan API Key gratis di https://makersuite.google.com/app/apikey"
    )
    
    st.markdown("---")
    st.markdown("**📌 Cara mendapatkan API Key:**")
    st.markdown("""
    1. Buka [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
    2. Login dengan akun Google
    3. Klik 'Create API Key'
    4. Copy dan paste di sini
    """)
    
    st.markdown("---")
    st.markdown("**📖 Tentang Chatbot**")
    st.markdown("""
    Chatbot ini dibuat khusus untuk menjawab 
    pertanyaan seputar Ilmu Tajwid.
    
    *Versi 1.0*
    """)

# ============================================
# FITUR CEK TOPIK TAJWID
# ============================================
kata_kunci_tajwid = [
    # Hukum Nun Mati/Tanwin
    "izhar", "idgham", "bighunnah", "bilaghunnah", "iqlab", "ikhfa",
    "nun mati", "tanwin", "nun sukun",
    
    # Hukum Mim Mati
    "ikhfa syafawi", "idgham mimi", "izhar syafawi", "mim mati", "mim sukun",
    
    # Hukum Mad
    "mad", "mad thabi'i", "mad far'i", "mad wajib muttasil", "mad jaiz munfasil",
    "mad lazim", "mad arid lissukun", "mad lin", "mad badal", "mad iwad",
    "tanda panjang", "harakat",
    
    # Lain-lain
    "ghunnah", "qalqalah", "qalqalah sugra", "qalqalah kubra",
    "ra tafkhim", "ra tarqiq", "lam jalalah",
    "waqaf", "wasal", "tanda waqaf", "saktah",
    "makhraj", "sifat huruf", "tajwid", "bacaan",
    "al-qur'an", "quran", "mengaji", "tartil", "hukum bacaan"
]

def cek_topik_tajwid(pertanyaan):
    """Memeriksa apakah pertanyaan terkait tajwid"""
    if not pertanyaan:
        return False
    
    pertanyaan = pertanyaan.lower()
    
    for kata in kata_kunci_tajwid:
        if kata in pertanyaan:
            return True
    
    # Cek kata kunci umum
    if "hukum" in pertanyaan and ("bacaan" in pertanyaan or "nun" in pertanyaan or "mim" in pertanyaan):
        return True
    
    return False

# ============================================
# INISIALISASI RIWAYAT CHAT
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# INPUT CHAT DARI USER
# ============================================
if prompt := st.chat_input("Tanyakan sesuatu tentang tajwid..."):
    
    # CEK: API Key sudah diisi?
    if not api_key:
        with st.chat_message("assistant"):
            st.error("⚠️ **API Key belum dimasukkan!**")
            st.info("Silakan masukkan API Key Gemini Anda di sidebar (sebelah kiri).")
        st.stop()
    
    # Tampilkan pertanyaan user
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simpan pertanyaan
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # CEK: Apakah pertanyaan tentang tajwid?
    if not cek_topik_tajwid(prompt):
        with st.chat_message("assistant"):
            st.warning("⚠️ Maaf, saya hanya bisa menjawab pertanyaan seputar **Ilmu Tajwid**.")
            st.info("""
            **Contoh pertanyaan yang bisa diajukan:**
            - Apa itu idgham bighunnah?
            - Jelaskan hukum mad jaiz munfasil
            - Perbedaan qalqalah sugra dan kubra
            - Bagaimana cara membaca ra tafkhim?
            - Contoh ikhfa dalam Al-Qur'an
            """)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Maaf, saya hanya bisa menjawab pertanyaan seputar Ilmu Tajwid."
        })
        st.stop()
    
    # ========================================
    # MEMANGGIL API GEMINI
    # ========================================
    try:
        # Konfigurasi API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Tampilkan loading
        with st.chat_message("assistant"):
            with st.spinner("🔍 Mencari jawaban..."):
                # Buat prompt khusus untuk tajwid
                prompt_tajwid = f"""
Anda adalah seorang ahli tajwid yang berpengalaman. Jawab pertanyaan berikut dengan:

1. Penjelasan yang jelas dan mudah dipahami
2. Sertakan contoh dari Al-Qur'an jika memungkinkan
3. Gunakan istilah tajwid yang tepat
4. Berikan cara praktis untuk mengingat/menerapkannya

Pertanyaan: {prompt}
"""
                
                # Kirim ke Gemini
                response = model.generate_content(prompt_tajwid)
                
                # Tampilkan jawaban
                st.markdown(response.text)
                
                # Tambahkan footer
                st.caption("---\n📖 Sumber: Chatbot Tajwid berbasis AI")
        
        # Simpan jawaban
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ Terjadi error: {e}")
            st.info("""
            **Kemungkinan penyebab:**
            - API Key salah atau tidak valid
            - Kuota API habis (60 request/menit gratis)
            - Masalah koneksi
            
            Coba periksa API Key Anda di sidebar.

            """)
