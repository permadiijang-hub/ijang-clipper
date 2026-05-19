import streamlit as st
from moviepy.editor import VideoFileClip
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="IjangPermadi97 Video Clipper", page_icon="✂️", layout="centered")

# --- KREDENSIAL LOGIN ---
USER_CORRECT = "permadi"
PASSWORD_CORRECT = "ijangpermadi"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- HALAMAN LOGIN ---
def login_page():
    st.title("🔐 Login Dashboard Kreator")
    st.write("Selamat datang di **ijangpermadi97.streamlit.app**")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Masuk"):
        if username == USER_CORRECT and password == PASSWORD_CORRECT:
            st.session_state.logged_in = True
            st.success("Login Berhasil!")
            st.rerun()
        else:
            st.error("Username atau Password salah.")

# --- HALAMAN UTAMA (VIDEO CLIPPER) ---
def main_page():
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.title("✂️ Potong & Kliping Video")
    st.write("Dashboard Kreator Gratis: **ijangpermadi97.streamlit.app**")
    st.markdown("---")
    
    # 1. Unggah Video
    uploaded_file = st.file_uploader("Unggah Video Mentah Anda (MP4, MOV)", type=["mp4", "mov"])
    
    if uploaded_file is not None:
        temp_in = "temp_raw_video.mp4"
        with open(temp_in, "wb") as f:
            f.write(uploaded_file.read())
            
        clip = VideoFileClip(temp_in)
        durasi_total = clip.duration
        
        st.info(f"Video berhasil dimuat. Total durasi: {durasi_total:.2f} detik.")
        st.video(temp_in)
        
        st.markdown("### 🛠️ Pengaturan Kliping")
        
        # 2. Input Waktu Potong
        start_time = st.number_input("Waktu Mulai (Detik ke-)", min_value=0.0, max_value=durasi_total, value=0.0, step=1.0)
        end_time = st.number_input("Waktu Selesai (Detik ke-)", min_value=0.0, max_value=durasi_total, value=min(durasi_total, 60.0), step=1.0)
        
        # 3. Opsi Format
        format_output = st.selectbox("Format Output Video", ["Tetap Asli (Landscape/Original)", "Ubah ke Vertikal (9:16 untuk TikTok/Shorts)"])
        
        if st.button("Buat Kliping Video"):
            if start_time >= end_time:
                st.error("Waktu mulai harus lebih kecil dari waktu selesai!")
            else:
                with st.spinner("Sedang memotong dan memproses video... Harap tunggu."):
                    try:
                        sub_clip = clip.subclip(start_time, end_time)
                        
                        if format_output == "Ubah ke Vertikal (9:16 untuk TikTok/Shorts)":
                            w, h = sub_clip.size
                            target_w = int(h * 9 / 16)
                            if target_w <= w:
                                x_center = w / 2
                                sub_clip = sub_clip.crop(x1=x_center - target_w/2, y1=0, x2=x_center + target_w/2, y2=h)
                        
                        output_clip_path = "output_kliping.mp4"
                        sub_clip.write_videofile(output_clip_path, codec="libx264", audio_codec="aac")
                        
                        st.success("Kliping video berhasil dibuat!")
                        st.video(output_clip_path)
                        
                        with open(output_clip_path, "rb") as file:
                            st.download_button(
                                label="📥 Unduh Hasil Kliping",
                                data=file,
                                file_name="kliping_ijangpermadi97.mp4",
                                mime="video/mp4"
                            )
                        
                        sub_clip.close()
                        if os.path.exists(output_clip_path):
                            os.remove(output_clip_path)
                            
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
        
        clip.close()
        if os.path.exists(temp_in):
            os.remove(temp_in)

# --- ALUR APLIKASI ---
if st.session_state.logged_in:
    main_page()
else:
    login_page()
