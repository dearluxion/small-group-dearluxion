import streamlit as st
import os
import json
import datetime
import re
import time
import base64

# --- 1. ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Small Group by Dearluxion", page_icon="🍸", layout="centered")

# CSS: ตกแต่งธีม
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E6EDF3; }
    
    /* การ์ดโพสต์ */
    .work-card-base {
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363D;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    .work-card-base:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.5);
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
        border-color: #A370F7;
        color: #A370F7;
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

    /* ป้ายราคา */
    .price-tag {
        background-color: #A370F7;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(163, 112, 247, 0.5);
    }
    
    /* Animation น้องไมล่า */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    .cute-guide {
        animation: bounce 2s infinite;
        background: linear-gradient(45deg, #FF9A9E, #FECFEF);
        padding: 10px 20px;
        border-radius: 30px;
        color: #555;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(255, 154, 158, 0.5);
        cursor: pointer;
    }
    
    a { color: #A370F7 !important; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- 2. ระบบจัดการไฟล์ ---
DB_FILE = "portfolio_db.json"
PROFILE_FILE = "profile_db.json"

def load_data():
    if not os.path.exists(DB_FILE): return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def save_data(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
    except: st.error("บันทึกโพสต์ไม่สำเร็จ")

def load_profile():
    if not os.path.exists(PROFILE_FILE): return {}
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_profile(data):
    try:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
    except: st.error("บันทึกโปรไฟล์ไม่สำเร็จ")

def get_base64_image(image_path):
    if not os.path.exists(image_path): return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Session Init
if 'liked_posts' not in st.session_state: st.session_state['liked_posts'] = []
if 'last_comment_time' not in st.session_state: st.session_state['last_comment_time'] = 0
if 'show_shop' not in st.session_state: st.session_state['show_shop'] = False
if 'is_admin' not in st.session_state: st.session_state['is_admin'] = False

# --- 3. Sidebar (เมนู & Q&A) ---
st.sidebar.title("🍸 เมนูหลัก")

# ระบบ Q&A คุยกับไมล่า
with st.sidebar.expander("🧚‍♀️ ถาม-ตอบ กับไมล่า (Q&A)", expanded=True):
    st.markdown("### 💬 อยากรู้อะไรถามไมล่าได้เลย!")
    q_options = [
        "เลือกคำถาม...",
        "🤔 อยากโพสต์เรื่องราวบ้างต้องทำไง?",
        "🛍️ สนใจสินค้า ซื้อยังไง?",
        "💻 เว็บนี้ใครสร้างครับ?",
        "🧚‍♀️ ไมล่าคือใครคะ?",
        "📞 ติดต่อบอส Dearluxion ได้ที่ไหน?"
    ]
    selected_q = st.selectbox("เลือกคำถาม:", q_options, label_visibility="collapsed")
    
    if selected_q == "🤔 อยากโพสต์เรื่องราวบ้างต้องทำไง?":
        st.info("🧚‍♀️ **ไมล่า:** ไม่ได้น้า~ นี่เป็น **พื้นที่ส่วนตัวของบอส Dearluxion** เท่านั้นค่ะ! แต่พี่ๆ สามารถกดไลก์และคอมเมนต์ให้กำลังใจบอสได้ตลอดเลยนะคะ 💖")
    elif selected_q == "🛍️ สนใจสินค้า ซื้อยังไง?":
        st.success("🧚‍♀️ **ไมล่า:** ง่ายมาก! กดปุ่ม **'สนใจสั่งซื้อ'** ในโพสต์ขายของ ระบบจะพาวาร์ปไปหาไอจีบอสทันทีเลยค่ะ 🚀")
    elif selected_q == "💻 เว็บนี้ใครสร้างครับ?":
        st.warning("🧚‍♀️ **ไมล่า:** **ท่าน Dearluxion สร้างเองกับมือ** ด้วยภาษา Python ล้วนๆ ค่ะ! เทพสุดๆ ไปเลยใช่มั้ยล่ะ? 😎 \n\nสนใจผลงานเพิ่มเติมติดตามได้ในเว็บนี้หรือ IG บอสเลยค่ะ!")
    elif selected_q == "🧚‍♀️ ไมล่าคือใครคะ?":
        st.write("🧚‍♀️ **ไมล่า:** หนูคือผู้ช่วยแสนน่ารักของบอสเองค่ะ! คอยดูแลพี่ๆ ทุกคนในเว็บนี้ ฝากเนื้อฝากตัวด้วยนะคะ ✨")
    elif selected_q == "📞 ติดต่อบอส Dearluxion ได้ที่ไหน?":
        st.error("🧚‍♀️ **ไมล่า:** จิ้มที่ลิงก์ Discord หรือ IG ตรงหน้าโปรไฟล์ด้านบนได้เลยค่ะ บอสตอบไวมาก! (ถ้าไม่หลับ 😴)")

st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 ค้นหา...", placeholder="พิมพ์คำค้นหา")

posts = load_data()
all_hashtags = set()
if posts:
    for p in posts:
        tags = re.findall(r"#([\w\u0E00-\u0E7F]+)", p['content'])
        for t in tags: all_hashtags.add(f"#{t}")

st.sidebar.markdown("### 📂 โซนของคุณ")
if st.session_state['show_shop']:
    st.sidebar.info("🛒 กำลังดูร้านค้า")
    if st.sidebar.button("🏠 กลับหน้าหลัก"):
        st.session_state['show_shop'] = False
        st.rerun()
else:
    selected_zone = st.sidebar.radio("หมวดหมู่:", ["🏠 รวมทุกโซน"] + sorted(list(all_hashtags)))

st.sidebar.markdown("---")

# --- LOGIN (ซ่อนรหัสแบบลับๆ) ---
if not st.session_state['is_admin']:
    with st.sidebar.expander("🔐 เข้าสู่ระบบ"):
        username = st.text_input("ไอดี")
        password = st.text_input("รหัสผ่าน", type="password")
        if st.button("ไขกุญแจ"):
            # [SECURITY TIP] รหัสถูกซ่อนไว้ด้วยการกลับด้าน (Reverse String)
            # คนมาส่องโค้ดจะงงว่า noixulraed คืออะไร (มันคือ dearluxion กลับหลัง!)
            secret_user = "noixulraed"[::-1] 
            secret_pass = "cm1212132121"[::-1] 
            
            if username == secret_user and password == secret_pass:
                st.session_state['is_admin'] = True
                st.rerun()
            else: 
                st.sidebar.error("ผิดครับ! (ไปแอบดูในโค้ดก็ไม่เจอหรอก 😜)")
else:
    st.sidebar.success("ยินดีต้อนรับบอส! 🕶️")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state['is_admin'] = False
        st.rerun()

# --- 4. Header & Profile ---
profile_data = load_profile()
user_emoji = profile_data.get('emoji', '😎') 

# ระบบสอนเปิดเมนู
if not st.session_state['is_admin']:
    st.info("🧚‍♀️ **ไมล่าบอกทาง:** พี่จ๋า~ กดลูกศร **มุมซ้ายบน** ↖️ เพื่อเปิดเมนูคุยกับไมล่า หรือค้นหาโพสต์ได้เลยนะคะ!")

top_col1, top_col2 = st.columns([8, 1])
with top_col1:
    col_p1, col_p2 = st.columns([1.5, 6])
    with col_p1:
        st.markdown(f"""
            <div style="font-size: 60px; line-height: 1; filter: drop-shadow(0 0 10px #A370F7); text-align: center; cursor:default;">
                {user_emoji}
            </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown(f"### 🍸 {profile_data.get('name', 'Dearluxion')}")
        st.markdown(f"_{profile_data.get('bio', '...')}_")
        links = []
        if profile_data.get('discord'): links.append(f"[Discord]({profile_data['discord']})")
        if profile_data.get('ig'): links.append(f"[Instagram]({profile_data['ig']})")
        if profile_data.get('extras'):
            for line in profile_data['extras'].split('\n'):
                if line.strip(): links.append(f"[{line.strip()}]({line.strip()})")
        st.markdown(" | ".join(links))

with top_col2:
    if st.button("🛒", help="ไปช้อปปิ้ง"):
        st.session_state['show_shop'] = True
        st.rerun()

st.markdown("---")

# --- 5. Admin Panel ---
if st.session_state['is_admin']:
    tab_post, tab_profile = st.tabs(["📝 เขียน / ขายของ", "👤 แก้ไขโปรไฟล์"])
    
    with tab_post:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_desc = st.text_area("เนื้อหา (Story)", height=150)
        with col2:
            new_img = st.file_uploader("รูป", type=['png','jpg'])
            new_video = st.file_uploader("คลิป", type=['mp4','mov'])
            post_color = st.color_picker("สีธีม", "#A370F7")
            price = st.number_input("💰 ราคา (ใส่ 0 = ไม่ขาย)", min_value=0, value=0)

        if st.button("🚀 โพสต์เลย", use_container_width=True):
            if new_desc:
                img_path = None
                if new_img:
                    img_path = new_img.name
                    with open(img_path, "wb") as f: f.write(new_img.getbuffer())
                
                video_path = None
                if new_video:
                    video_path = new_video.name
                    with open(video_path, "wb") as f: f.write(new_video.getbuffer())
                
                new_post = {
                    "id": str(datetime.datetime.now().timestamp()),
                    "date": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "content": new_desc,
                    "image": img_path,
                    "video": video_path,
                    "color": post_color,
                    "price": price,
                    "likes": 0,
                    "comments": []
                }
                current = load_data()
                current.append(new_post)
                save_data(current)
                st.success("เรียบร้อย!")
                time.sleep(1); st.rerun()
            else: st.warning("พิมพ์อะไรหน่อยสิครับ")

    with tab_profile:
        with st.form("pf_form"):
            p_name = st.text_input("ชื่อ", value=profile_data.get('name', 'Dearluxion'))
            p_emoji = st.text_input("อิโมจิประจำตัว (ใส่แทนรูป)", value=profile_data.get('emoji', '😎'))
            p_bio = st.text_input("Bio", value=profile_data.get('bio', ''))
            p_discord = st.text_input("Discord URL", value=profile_data.get('discord',''))
            p_ig = st.text_input("IG URL", value=profile_data.get('ig',''))
            p_ex = st.text_area("ลิงก์อื่นๆ (บรรทัดละลิงก์)", value=profile_data.get('extras',''))
            
            if st.form_submit_button("บันทึก"):
                save_profile({
                    "name": p_name, 
                    "emoji": p_emoji,
                    "bio": p_bio, 
                    "discord": p_discord, 
                    "ig": p_ig, 
                    "extras": p_ex
                })
                st.success("อัปเดตแล้ว!")
                st.rerun()
        if st.button("ลบโปรไฟล์"):
            if os.path.exists(PROFILE_FILE): os.remove(PROFILE_FILE)
            st.rerun()
    st.markdown("---")

# --- 6. Feed Display ---
filtered = posts
if st.session_state['show_shop']:
    st.markdown("## 🛒 ร้านค้า (Shop Zone)")
    
    with st.expander("🧚‍♀️ พี่จ๋า~ หาทางกลับไม่เจอเหรอคะ? (จิ้มไมล่าสิ!) 💖", expanded=True):
        st.markdown("""
            <div class="cute-guide">
                ✨ ทางลัดพิเศษสำหรับพี่คนโปรดของไมล่า! 🌈
            </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏠 กลับบ้านกับไมล่า!", use_container_width=True):
                st.session_state['show_shop'] = False
                st.balloons()
                time.sleep(1)
                st.rerun()
        with c2: st.info("👈 กดปุ่มนี้ ไมล่าจะพาพี่กลับหน้าหลักเองค่ะ!")

    filtered = [p for p in filtered if p.get('price', 0) > 0 or "#ร้านค้า" in p['content']]
    if not filtered: st.warning("ยังไม่มีสินค้าวางขายจ้า")
else:
    if selected_zone != "🏠 รวมทุกโซน": filtered = [p for p in filtered if selected_zone in p['content']]
    if search_query: filtered = [p for p in filtered if search_query.lower() in p['content'].lower()]

if filtered:
    for post in reversed(filtered):
        accent = post.get('color', '#A370F7')
        
        with st.container():
            col_head, col_del = st.columns([0.85, 0.15])
            with col_head:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                    <div style="font-size:40px; line-height:1; filter: drop-shadow(0 0 5px {accent});">{user_emoji}</div>
                    <div style="line-height:1.2;">
                        <div style="font-size:18px; font-weight:bold; color:#E6EDF3;">
                            {profile_data.get('name', 'Dearluxion')} 
                            <span style="color:{accent}; font-size:14px;">🛡️ Verified</span>
                        </div>
                        <div style="font-size:12px; color:#8B949E;">{post['date']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_del:
                if st.session_state['is_admin']:
                    if st.button("🗑️", key=f"del_{post['id']}"):
                        all_p = load_data()
                        save_data([x for x in all_p if x['id'] != post['id']])
                        st.rerun()

            if post.get('image') and os.path.exists(post['image']): st.image(post['image'], use_container_width=True)
            if post.get('video') and os.path.exists(post['video']): st.video(post['video'])
            
            content = post['content']
            yt = re.search(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', content)
            if yt: st.video(f"https://youtu.be/{yt.group(6)}")
            
            st.markdown(f"""<div class="work-card-base" style="border-left: 5px solid {accent};">{content}</div>""", unsafe_allow_html=True)
            
            price = post.get('price', 0)
            if price > 0:
                st.markdown(f"<div class='price-tag'>💰 ราคา: {price:,} บาท</div>", unsafe_allow_html=True)
                buy_link = profile_data.get('ig') or profile_data.get('discord') or "#"
                st.markdown(f"""<a href="{buy_link}" target="_blank"><button style="background-color:{accent}; color:white; border:none; padding:8px 16px; border-radius:8px; width:100%; cursor:pointer;">🛍️ สนใจสั่งซื้อ (คลิก)</button></a><br><br>""", unsafe_allow_html=True)

            c_a, c_b = st.columns([1, 2])
            with c_a:
                liked = post['id'] in st.session_state['liked_posts']
                if st.button(f"{'❤️' if liked else '🤍'} {post['likes']}", key=f"l_{post['id']}", disabled=liked):
                    if not liked:
                        d = load_data()
                        for x in d: 
                            if x['id'] == post['id']: x['likes']+=1; break
                        save_data(d)
                        st.session_state['liked_posts'].append(post['id'])
                        st.toast("🧚‍♀️ ไมล่า: ขอบคุณที่ชอบโพสต์ของบอสนะคะ! จุ๊บๆ 💋💖", icon="😍")
                        st.rerun()
            
            with c_b:
                with st.expander(f"💬 ({len(post['comments'])})"):
                    if post['comments']:
                        for i, c in enumerate(post['comments']):
                            cx, cy = st.columns([0.9, 0.1])
                            with cx: st.markdown(f"<div class='comment-box'><b>{c['user']}:</b> {c['text']}</div>", unsafe_allow_html=True)
                            with cy:
                                if st.session_state['is_admin'] and st.button("x", key=f"dc_{post['id']}_{i}"):
                                    d = load_data()
                                    for x in d:
                                        if x['id'] == post['id']: x['comments'].pop(i); break
                                    save_data(d); st.rerun()
                    
                    with st.form(key=f"cf_{post['id']}"):
                        u = st.text_input("ชื่อ", placeholder="ชื่อเล่น...", label_visibility="collapsed")
                        t = st.text_input("ข้อความ", placeholder="คอมเมนต์...", label_visibility="collapsed")
                        if st.form_submit_button("ส่ง"):
                            now = time.time()
                            if now - st.session_state['last_comment_time'] < 35:
                                st.toast(f"รออีก {35 - int(now - st.session_state['last_comment_time'])} วินาทีนะจ๊ะ ⏳", icon="⛔")
                            elif t:
                                d = load_data()
                                for x in d:
                                    if x['id'] == post['id']: x['comments'].append({"user": u if u else "Guest", "text": t}); break
                                save_data(d)
                                st.session_state['last_comment_time'] = now
                                st.rerun()
            st.markdown("___")
else:
    if not st.session_state['show_shop']: st.info("ยังไม่มีโพสต์ครับ")

st.markdown("<br><center><small style='color:#A370F7'>Small Group by Dearluxion © 2025</small></center>", unsafe_allow_html=True)