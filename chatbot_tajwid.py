import streamlit as st
from pytgpt.opengpts import OPENGPT
import time

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="Chatbot Ilmu Tajwid - GRATIS",
    page_icon="🕌",
    layout="centered"
)

# ============================================
# JUDUL DAN DESKRIPSI
# ============================================
st.title("🕌 Chatbot Ilmu Tajwid")
st.markdown("### GRATIS - TANPA PERLU API KEY!")

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
# SIDEBAR (INFORMASI)
# ============================================
with st.sidebar:
    st.header("📖 Informasi")
    st.markdown("""
    **Chatbot GRATIS** ini menggunakan teknologi AI tanpa perlu API Key.
    
    **Cara pakai:**
    1. Langsung tanya di kolom chat
    2. Tunggu jawaban
    3. Selesai!
    
    **Provider yang digunakan:** Phind (gratis)
    """)
    
    st.markdown("---")
    st.markdown("**📌 Tips:**")
    st.markdown("""
    - Tanyakan dengan jelas
    - Bisa minta contoh ayat
    - Chatbot hanya menjawab seputar tajwid
    """)
    
    st.markdown("---")
    st.markdown("**🕌 Tentang Chatbot**")
    st.markdown("""
    Chatbot ini dibuat khusus untuk 
    membantu belajar Ilmu Tajwid.
    
    *Versi 2.0 - Tanpa API Key*
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
# INISIALISASI BOT (CUKUP SEKALI)
# ============================================
@st.cache_resource
def init_bot():
    """Inisialisasi bot Phind (gratis, tanpa API Key)"""
    try:
        return PHIND()
    except Exception as e:
        st.error(f"Gagal inisialisasi bot: {e}")
        return None

# Panggil inisialisasi bot
bot = OPENGPT()

if bot is None:
    st.error("⚠️ Bot gagal diinisialisasi. Coba refresh halaman.")
    st.stop()

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
    # MEMANGGIL BOT TANPA API KEY
    # ========================================
    try:
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
                
                # Kirim ke bot (TANPA API KEY!)
                response = bot.chat(prompt_tajwid)
                
                # Tampilkan jawaban
                st.markdown(response)
                
                # Tambahkan footer
                st.caption("---\n📖 Sumber: Chatbot Tajwid (Gratis - Tanpa API Key)")
        
        # Simpan jawaban
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ Terjadi error: {e}")
            st.info("""
            **Kemungkinan penyebab:**
            - Provider sedang sibuk
            - Koneksi internet bermasalah
            - Coba tanya ulang atau refresh halaman
            
            Atau coba tanya dengan pertanyaan yang lebih spesifik.
            """)

