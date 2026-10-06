import streamlit as st
import random
import time
import os
import base64

# Cấu hình trang Streamlit
st.set_page_config(page_title="Oẳn Tù Tì với AN NHI", page_icon="💖", layout="centered")

# Hàm chuyển đổi ảnh local sang dạng Base64 để nhúng thẳng vào CSS background
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Hàm phát âm thanh bằng HTML5 Audio
def get_audio_html(file_path, autoplay=True, loop=False):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            loop_attr = "loop" if loop else ""
            auto_attr = "autoplay" if autoplay else ""
            return f"""
                <audio {auto_attr} {loop_attr} hidden>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
    return ""

# Lấy dữ liệu ảnh mã hóa base64
img_p1_b64 = get_base64_of_bin_file("p1.jpg")
img_cpu_b64 = get_base64_of_bin_file("cpu.jpg")

# Khởi tạo trạng thái game (Session State)
if 'p1_hp' not in st.session_state:
    st.session_state.p1_hp = 100
if 'cpu_hp' not in st.session_state:
    st.session_state.cpu_hp = 100
if 'last_p1_move' not in st.session_state:
    st.session_state.last_p1_move = "✊"
if 'last_cpu_move' not in st.session_state:
    st.session_state.last_cpu_move = "✊"
if 'result_text' not in st.session_state:
    st.session_state.result_text = "Thách bạn thắng được AN NHI đấy! 😏"

MOVES = {
    "Búa (A)": "✊",
    "Bao (S)": "✋",
    "Kéo (D)": "✌️"
}

# Thuật toán gian lận: P1 chỉ có 10% tỷ lệ thắng
def get_an_nhi_move(p1_move):
    r = random.random()
    if r < 0.10:   # 10% P1 Thắng
        if p1_move == "✊": return "✌️"
        if p1_move == "✋": return "✊"
        if p1_move == "✌️": return "✋"
    elif r < 0.20: # 10% Hòa
        return p1_move
    else:          # 80% AN NHI Thắng (Bắt bài P1)
        if p1_move == "✊": return "✋"
        if p1_move == "✋": return "✌️"
        if p1_move == "✌️": return "✊"

def play(user_choice_key):
    if st.session_state.p1_hp <= 0 or st.session_state.cpu_hp <= 0:
        return

    p1_move = MOVES[user_choice_key]
    cpu_move = get_an_nhi_move(p1_move)

    # Hiệu ứng đếm ngược 1... 2... 3...
    countdown_box = st.empty()
    for count in ["1...", "2...", "3...", "RA CHIÊU! 💥"]:
        countdown_box.markdown(f"""
            <div style="text-align: center; font-size: 42px; font-weight: bold; color: #FFD700; text-shadow: 2px 2px 8px #000;">
                {count}
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.4)
    countdown_box.empty()

    st.session_state.last_p1_move = p1_move
    st.session_state.last_cpu_move = cpu_move

    # Tính toán dame và kết quả
    if p1_move == cpu_move:
        st.session_state.result_text = "🤝 HÒA RỒI! AN NHI tha cho bạn hiệp này!"
    elif (p1_move == "✊" and cpu_move == "✌️") or \
         (p1_move == "✋" and cpu_move == "✊") or \
         (p1_move == "✌️" and cpu_move == "✋"):
        damage = random.randint(15, 25)
        st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - damage)
        st.session_state.result_text = f"🔥 HỮU DUYÊN! Bạn hên thắng được AN NHI! Gây {damage} sát thương!"
    else:
        damage = random.randint(20, 30)
        st.session_state.p1_hp = max(0, st.session_state.p1_hp - damage)
        st.session_state.result_text = f"💥 AN NHI BẮT BÀI! Bạn bị vả {damage} HP!"

def reset_game():
    st.session_state.p1_hp = 100
    st.session_state.cpu_hp = 100
    st.session_state.last_p1_move = "✊"
    st.session_state.last_cpu_move = "✊"
    st.session_state.result_text = "Ván mới bắt đầu! Cố lên nhé!"

# Tùy chỉnh CSS giao diện nền chia đôi trái/phải và làm mờ ảnh
st.markdown(f"""
<style>
    /* Nền chia làm 2 bên trái/phải có hình mờ */
    .stApp {{
        position: relative;
        background-color: #111;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 50%; height: 100%;
        background-image: url("data:image/jpeg;base64,{img_p1_b64}");
        background-size: cover;
        background-position: center;
        opacity: 0.35;
        z-index: 0;
    }}
    .stApp::after {{
        content: "";
        position: absolute;
        top: 0; right: 0; width: 50%; height: 100%;
        background-image: url("data:image/jpeg;base64,{img_cpu_b64}");
        background-size: cover;
        background-position: center;
        opacity: 0.35;
        z-index: 0;
    }}
    
    /* Lớp nội dung đè lên trên nền */
    .main .block-container {{
        position: relative;
        z-index: 1;
        background: rgba(0, 0, 0, 0.45);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(3px);
    }}

    .header-title {{
        text-align: center;
        font-weight: 900;
        font-size: 36px;
        color: #FF69B4;
        text-shadow: 2px 2px 6px #000;
        margin-bottom: 20px;
    }}

    .hp-bar-container {{
        background-color: #333;
        border-radius: 12px;
        border: 2px solid #FFF;
        overflow: hidden;
        height: 22px;
        margin-top: 5px;
    }}
    .hp-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #00FF7F, #3CB371);
        transition: width 0.3s ease;
    }}

    .hand-display {{
        font-size: 100px;
        text-align: center;
        filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.8));
    }}

    .result-box {{
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #FFF;
        padding: 12px;
        background-color: rgba(255, 20, 147, 0.85);
        border-radius: 15px;
        border: 2px solid #FFF;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
        margin: 15px 0;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">💖 OẮN TÙ TÌ CÙNG AN NHI 💖</div>', unsafe_allow_html=True)

# Hiển thị Avatar & Thanh HP
col1, col_mid, col2 = st.columns([4, 1, 4])

with col1:
    st.markdown("<h3 style='color: #00FFFF; text-align: center; text-shadow: 1px 1px 3px #000;'>🐶 P1 (BẠN)</h3>", unsafe_allow_html=True)
    if os.path.exists("p1.jpg"):
        st.image("p1.jpg", use_container_width=True)
    st.markdown(f'''
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.p1_hp}%;"></div>
    </div>
    <p style="text-align: center; font-weight: bold; color: white;">HP: {st.session_state.p1_hp}/100</p>
    ''', unsafe_allow_html=True)

with col_mid:
    st.markdown("<h2 style='text-align: center; color: #FFD700; margin-top: 50px; text-shadow: 2px 2px 4px #000;'>VS</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color: #FF69B4; text-align: center; text-shadow: 1px 1px 3px #000;'>👧 AN NHI</h3>", unsafe_allow_html=True)
    if os.path.exists("cpu.jpg"):
        st.image("cpu.jpg", use_container_width=True)
    st.markdown(f'''
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.cpu_hp}%;"></div>
    </div>
    <p style="text-align: center; font-weight: bold; color: white;">HP: {st.session_state.cpu_hp}/100</p>
    ''', unsafe_allow_html=True)

st.divider()

# Bàn tay ra chiêu
hand_col1, hand_col2 = st.columns(2)
with hand_col1:
    st.markdown(f'<div class="hand-display">{st.session_state.last_p1_move}</div>', unsafe_allow_html=True)
with hand_col2:
    st.markdown(f'<div class="hand-display" style="transform: scaleX(-1);">{st.session_state.last_cpu_move}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="result-box">{st.session_state.result_text}</div>', unsafe_allow_html=True)

# Xử lý Nhạc Nền & Trạng Thái Thắng / Thua
if st.session_state.p1_hp <= 0:
    st.markdown(get_audio_html("lose.mp3", autoplay=True, loop=False), unsafe_allow_html=True)
    st.error("💀 BẠN ĐÃ THUA AN NHI TÂM PHỤC KHẨU PHỤC!")
    st.snow()
    if st.button("Chơi lại để gỡ gạc 🔄", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.cpu_hp <= 0:
    st.markdown(get_audio_html("win.mp3", autoplay=True, loop=False), unsafe_allow_html=True)
    st.success("🎉 BÁ ĐẠO! Bạn đã đánh bại AN NHI (dù tỷ lệ thắng chỉ 10%)!")
    st.balloons()
    if st.button("Chơi ván nữa 🔄", use_container_width=True):
        reset_game()
        st.rerun()

else:
    st.markdown(get_audio_html("tiktok.mp3", autoplay=True, loop=True), unsafe_allow_html=True)

    st.markdown("<h4 style='color: white; text-align: center;'>🎯 Chọn nước đi của bạn:</h4>", unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button("✊ Búa (A)", use_container_width=True):
            play("Búa (A)")
            st.rerun()
    with btn2:
        if st.button("✋ Bao (S)", use_container_width=True):
            play("Bao (S)")
            st.rerun()
    with btn3:
        if st.button("✌️ Kéo (D)", use_container_width=True):
            play("Kéo (D)")
            st.rerun()