import streamlit as st
import os
import json
import datetime
import re
import time

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Small Group by Dearluxion", page_icon="🍸", layout="centered")

# CSS: ตกแต่งธีม Dark Mode + ฟอนต์สวยๆ
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E6EDF3; }
    
    /* การ์ดโพสต์ */
    .work-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363D;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* ปุ่มกด */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #30363D;
        background-color: #21262D;
        color: white;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #A370F7; /* เปลี่ยนสีธีมเป็นม่วงๆ ให้เข้ากับมาตินี่ */
        color: #A370F7;
    }
    
    /* ปุ่มที่กดไลก์แล้ว */
    button[disabled] {
        background-color: #3b2323 !important;
        color: #ff6b6b !important;
        border-color: #ff6b6b !important;
        opacity: 1 !important;
    }

    /* กล่องคอมเมนต์ */
    .comment-box {
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        margin-top: 8px;
        border-left: 3px solid #A370F7;
        font-size: 13px;
    }
    
    /* ลิงก์ */
    a { color: #A370F7 !important; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- 2. ระบบฐานข้อมูล ---
DB_FILE = "portfolio_db.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        st.error("เกิดข้อผิดพลาดในการบันทึกข้อมูล")

# เก็บค่า Session
if 'liked_posts' not in st.session_state:
    st.session_state['liked_posts'] = []

if 'last_comment_time' not in st.session_state:
    st.session_state['last_comment_time'] = 0

# --- 3. Sidebar Admin ---
st.sidebar.title("🔧 แผงควบคุม")

if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

if not st.session_state['is_admin']:
    with st.sidebar.expander("🔐 เฉพาะเจ้าของร้าน"):
        username = st.text_input("ไอดี")
        password = st.text_input("รหัสผ่าน", type="password")
        
        if st.button("ไขกุญแจ"):
            # อัปเดตรหัสผ่านตามที่ขอครับ
            if username == "dearluxion" and password == "1212312121mc":
                st.session_state['is_admin'] = True
                st.rerun()
            else:
                st.sidebar.error("รหัสไม่ถูกต้อง!")
else:
    st.sidebar.success("ยินดีต้อนรับครับบอส ✅")
    st.sidebar.write("User: **Dearluxion**")
    if st.sidebar.button("ล็อกเอาท์"):
        st.session_state['is_admin'] = False
        st.rerun()

# --- 4. Header (เปลี่ยนข้อความตรงนี้) ---
st.markdown("""
    <h1 style='text-align: center; background: -webkit-linear-gradient(45deg, #A370F7, #00D4FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
    🍸 Small Group by Dearluxion
    </h1>
    <p style='text-align: center; color: #8B949E; font-style: italic;'>
    "มาตินี่แก้วนั้น มันน่าลิ้มลองอีกจัง"
    </p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- 5. Post Form (Admin) ---
if st.session_state['is_admin']:
    with st.container():
        st.subheader("📝 เขียนเรื่องราวใหม่")
        col1, col2 = st.columns([3, 1])
        with col1:
            new_desc = st.text_area("บรรยายความรู้สึก (ใส่ลิงก์ YouTube ได้)")
        with col2:
            new_img = st.file_uploader("รูปภาพ", type=['png', 'jpg', 'jpeg'])
        
        if st.button("🚀 โพสต์เลย"):
            if new_desc and len(new_desc.strip()) > 0:
                img_path = None
                if new_img:
                    img_path = new_img.name
                    with open(img_path, "wb") as f:
                        f.write(new_img.getbuffer())
                
                new_post = {
                    "id": str(datetime.datetime.now().timestamp()),
                    "date": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "content": new_desc,
                    "image": img_path,
                    "likes": 0,
                    "comments": []
                }
                
                posts = load_data()
                posts.append(new_post)
                save_data(posts)
                st.success("บันทึกความทรงจำแล้ว")
                st.rerun()
            else:
                st.warning("เขียนอะไรหน่อยสิครับ")
    st.markdown("---")

# --- 6. Feed Display ---
posts = load_data()

if posts:
    for i, post in enumerate(reversed(posts)):
        with st.container():
            # Header
            col_h1, col_h2 = st.columns([0.1, 0.9])
            with col_h1:
                st.write("🗓️")
            with col_h2:
                st.markdown(f"**{post['date']}** | 🛡️ **Dearluxion** <span style='color:#A370F7'>✓ Verified</span>", unsafe_allow_html=True)
            
            # Image
            if post['image'] and os.path.exists(post['image']):
                st.image(post['image'], use_container_width=True)
            
            content = post['content']
            
            # YouTube Auto Embed
            youtube_match = re.search(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', content)
            if youtube_match:
                st.video(f"https://youtu.be/{youtube_match.group(6)}")
            
            # Content Box
            st.markdown(f"""
            <div style="background-color:#161B22; padding:15px; border-radius:10px; border:1px solid #30363D; color:#E6EDF3; margin-top:10px;">
                {content}
            </div>
            """, unsafe_allow_html=True)
            
            # Buttons
            st.write("") 
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                has_liked = post['id'] in st.session_state['liked_posts']
                if has_liked:
                    st.button(f"❤️ {post['likes']} ถูกใจแล้ว", key=f"liked_btn_{post['id']}", disabled=True)
                else:
                    if st.button(f"🤍 {post['likes']} ถูกใจ", key=f"like_btn_{post['id']}"):
                        posts_data = load_data()
                        for p in posts_data:
                            if p['id'] == post['id']:
                                p['likes'] += 1
                                break
                        save_data(posts_data)
                        st.session_state['liked_posts'].append(post['id'])
                        st.rerun()

            with col_b:
                with st.expander(f"💬 ความคิดเห็น ({len(post['comments'])})"):
                    for c in post['comments']:
                        st.markdown(f"<div class='comment-box'><b>{c['user']}:</b> {c['text']}</div>", unsafe_allow_html=True)
                    
                    with st.form(key=f"comment_form_{post['id']}"):
                        col_c1, col_c2 = st.columns([1, 2])
                        with col_c1:
                            c_user = st.text_input("ชื่อ", placeholder="แขกรับเชิญ", label_visibility="collapsed")
                        with col_c2:
                            c_text = st.text_input("ข้อความ", placeholder="คอมเมนต์...", label_visibility="collapsed")
                        
                        # ปุ่มส่ง + Cooldown
                        submitted = st.form_submit_button("ส่ง 🥂")
                        if submitted:
                            if not c_text or len(c_text.strip()) == 0:
                                st.toast("พิมพ์ข้อความก่อนนะครับ", icon="⚠️")
                            else:
                                current_time = time.time()
                                if current_time - st.session_state['last_comment_time'] < 5:
                                    st.toast("⏳ จิบมาตินี่รอสัก 5 วินาทีนะ...", icon="⛔")
                                else:
                                    posts_data = load_data()
                                    for p in posts_data:
                                        if p['id'] == post['id']:
                                            p['comments'].append({
                                                "user": c_user if c_user else "Stranger",
                                                "text": c_text
                                            })
                                            break
                                    save_data(posts_data)
                                    st.session_state['last_comment_time'] = current_time
                                    st.toast("ส่งความคิดเห็นแล้ว", icon="✅")
                                    time.sleep(1)
                                    st.rerun()
            st.markdown("___")
else:
    st.info("ร้านยังว่างอยู่... รอเรื่องเล่าใหม่ๆ")

st.markdown("<br><center><small style='color:#A370F7'>Small Group by Dearluxion © 2025</small></center>", unsafe_allow_html=True)