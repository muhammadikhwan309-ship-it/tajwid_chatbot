import streamlit as st
import time
from pytgpt.leo import LEO

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
st.markdown("### GRATIS - Langsung Tanya!")

st.markdown("""
Assalamu'alaikum! 👋 Saya adalah chatbot khusus yang akan membantu Anda 
belajar **Ilmu Tajwid** (hukum bacaan Al-Qur'an).

**Topik yang bisa ditanyakan:**
- ✅ Hukum Nun Mati/Tanwin (Izhar, Idgham, Iqlab, Ikhfa)
- ✅ Hukum Mim Mati (Ikhfa Syafawi, Idgham Mimi, Izhar Syafawi)
- ✅ Hukum Mad (Mad Thabi'i, Mad Wajib, Mad Jaiz, dll)
- ✅ Qalqalah dan Ghunnah
- ✅ Makhraj dan Sifat Huruf
- ✅ Tanda Waqaf
""")

st.markdown("---")

# ============================================
# SIDEBAR INFORMASI
# ============================================
with st.sidebar:
    st.header("📖 Info Chatbot")
    st.markdown("""
    **Cara pakai:**
    1. Tanya di kolom chat
    2. Tunggu jawaban
    3. Selesai!
    
    **Provider:** Leo (Brave) - stabil
    """)
    
    st.markdown("---")
    st.markdown("**📌 Contoh pertanyaan:**")
    st.markdown("""
    - Apa itu idgham bighunnah?
    - Jelaskan hukum mad jaiz munfasil
    - Perbedaan qalqalah sugra dan kubra
    - Contoh ikhfa dalam Al-Qur'an
    - Kapan harus ghunnah?
    """)
    
    st.markdown("---")
    st.markdown("**🕌 About**")
    st.markdown("Chatbot Tajwid v2.0")

# ============================================
# DAFTAR KATA KUNCI TAJWID
# ============================================
kata_kunci_tajwid = [
    "izhar", "idgham", "iqlab", "ikhfa", "nun mati", "tanwin", "nun sukun",
    "ikhfa syafawi", "idgham mimi", "izhar syafawi", "mim mati", "mim sukun",
    "mad", "mad thabi'i", "mad far'i", "mad wajib muttasil", "mad jaiz munfasil",
    "mad lazim", "mad arid lissukun", "mad lin", "mad badal", "mad iwad",
    "ghunnah", "qalqalah", "qalqalah sugra", "qalqalah kubra",
    "ra tafkhim", "ra tarqiq", "lam jalalah",
    "waqaf", "wasal", "tanda waqaf", "saktah",
    "makhraj", "sifat huruf", "tajwid", "bacaan",
    "al-qur'an", "quran", "mengaji", "tartil", "hukum bacaan"
]

def cek_topik_tajwid(pertanyaan):
    """Cek apakah pertanyaan tentang tajwid"""
    if not pertanyaan:
        return False
    
    pertanyaan = pertanyaan.lower()
    
    for kata in kata_kunci_tajwid:
        if kata in pertanyaan:
            return True
    
    return False

# ============================================
# INISIALISASI BOT (LEO - PALING STABIL)
# ============================================
@st.cache_resource
def init_bot():
    """Inisialisasi bot Leo (gratis, stabil)"""
    try:
        bot = LEO()
        return bot
    except Exception as e:
        st.error(f"Gagal inisialisasi bot: {e}")
        return None

bot = init_bot()

# ============================================
# RIWAYAT CHAT
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# INPUT CHAT
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
            st.warning("⚠️ Maaf, saya hanya bisa menjawab pertanyaan seputar Ilmu Tajwid.")
            st.info("Contoh: apa itu idgham? jelaskan mad jaiz munfasil?")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Maaf, saya hanya bisa menjawab pertanyaan seputar Ilmu Tajwid."
        })
        st.stop()
    
    # CEK: Bot ready?
    if bot is None:
        with st.chat_message("assistant"):
            st.error("❌ Bot gagal diinisialisasi. Refresh halaman.")
        st.stop()
    
    # ========================================
    # MINTA JAWABAN DARI BOT
    # ========================================
    try:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Mencari jawaban..."):
                
                # Prompt khusus untuk tajwid
                prompt_tajwid = f"""Kamu adalah ahli tajwid. Jawab pertanyaan ini dengan:
- Penjelasan jelas dan mudah
- Berikan contoh dari Al-Qur'an
- Gunakan istilah tajwid yang tepat

Pertanyaan: {prompt}"""
                
                # Minta jawaban (dengan timeout)
                response = bot.chat(prompt_tajwid)
                
                # Tampilkan jawaban
                if response:
                    st.markdown(response)
                    st.caption("---\n📖 Sumber: Chatbot Tajwid (Gratis)")
                else:
                    st.error("Jawaban kosong. Coba lagi.")
        
        # Simpan jawaban
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ Error: {e}")
            st.info("Coba refresh atau tanya ulang.")

# ============================================
# TOMBOL RESET CHAT
# ============================================
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.rerun()
