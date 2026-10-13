import streamlit as st

# ==========================================
# INITIALIZATION & PAGE CONFIG
# ==========================================
IN_STORE_RATE = 50      # ค่าบริการเล่นในร้าน 50 บาท/คน/ชั่วโมง
LATE_FEE_RATE = 20      # ค่าปรับคืนเกมสาย 20 บาท/วัน/รายการ
MEMBER_DISCOUNT = 0.10  # ส่วนลดสมาชิก 10%
VAT_RATE = 0.07         # ภาษีมูลค่าเพิ่ม 7%

st.set_page_config(
    page_title="Game Shop Management 🎲☁️", 
    page_icon="🎨", 
    layout="centered"
)

# ==========================================
# CUSTOM CUTE PASTEL BLUE CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* พี้นหลังสีขาว-ฟ้าพาสเทลนุ่มนวล */
    .stApp {
        background-color: #f4f9ff;
        color: #2b4c7e;
    }
    
    /* กล่องข้อความ และ Container สไตล์การ์ตูนมนๆ */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input, 
    .stSelectbox > div > div > div {
        border-radius: 15px !important;
        border: 2px solid #b2d8d8 !important;
        background-color: #ffffff !important;
        color: #2b4c7e !important;
    }
    
    /* ตกแต่งปุ่มหลัก (Button) สีฟ้าพาสเทลน่ารัก */
    .stButton > button {
        border-radius: 20px !important;
        background: linear-gradient(135deg, #a8d8ea 0%, #aaabb8 100%);
        background-color: #89cff0 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(137, 207, 240, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(137, 207, 240, 0.6);
        background-color: #70c1e8 !important;
    }

    /* ตกแต่งวิดเจ็ต Radio Button */
    div[role="radiogroup"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 20px;
        border: 2px dashed #b8e2f2;
    }

    /* ตกแต่งส่วนใบเสร็จ */
    .stCodeBlock {
        border-radius: 15px !important;
        border: 2px solid #a8d8ea !important;
        background-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER SECTION
# ==========================================
st.markdown("<h1 style='text-align: center; color: #4a90e2;'>🎲 GAME SHOP MANAGEMENT ☁️✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7b9acc; font-size: 16px;'>🎀 ระบบคำนวณค่าบริการ เล่นในร้าน • เช่า • คืนเกม น่ารักสดใส 🧸🧃</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# USER INPUT: CUSTOMER & SERVICE SELECTION
# ==========================================
st.markdown("### 👤 ข้อมูลลูกค้า (Customer Info)")
customer_name_input = st.text_input("✨ Enter Customer Name (ชื่อลูกค้า):", value="", placeholder="เช่น น้องพะแพง / ลูกค้าทั่วไป")
customer_name = customer_name_input.strip() if customer_name_input.strip() != "" else "General Customer"

st.markdown("### 🛍️ เลือกประเภทบริการ (Select Service)")
service_option = st.radio(
    "Service Type:",
    ["1 = In-Store Play (เล่นในร้าน) 🎮", "2 = Game Rental Service (เช่าเกม) 📦", "3 = Game Return Service (คืนเกม/ค่าปรับ) 🔄"]
)

# แปลงตัวเลือกเป็น service_type INTEGER (1, 2, 3)
service_type = int(service_option.split("=")[0].strip())

subtotal = 0.0
discount = 0.0
total_after_discount = 0.0
vat = 0.0
net_total = 0.0

st.markdown("<hr style='border: 1px dashed #b8e2f2;'>", unsafe_allow_html=True)

# ==========================================
# PROCESS SERVICE SELECTION (SWITCH service_type)
# ==========================================

# CASE 1: In-Store Play
if service_type == 1:
    st.markdown("#### 🎮 CASE 1: In-Store Play (นั่งเล่นในร้าน ☕)")
    col1, col2 = st.columns(2)
    with col1:
        players = st.number_input("👥 จำนวนผู้เล่น (players > 0):", min_value=1, value=1, step=1)
    with col2:
        hours = st.number_input("⏰ จำนวนชั่วโมง (hours > 0):", min_value=1, value=1, step=1)
    
    subtotal = float(players * hours * IN_STORE_RATE)

# CASE 2: Game Rental Service
elif service_type == 2:
    st.markdown("#### 📦 CASE 2: Game Rental Service (เช่าเกมกลับบ้าน 🏠)")
    num_items = st.number_input("🧩 จำนวนเกมที่ต้องการเช่า (total games):", min_value=1, value=1, step=1)
    
    subtotal = 0.0
    for i in range(int(num_items)):
        st.markdown(f"**🎨 รายการเกมที่ #{i+1}**")
        col_name, col_rate, col_days = st.columns([2, 1, 1])
        with col_name:
            game_name = st.text_input(f"ชื่อเกม #{i+1}", value=f"Board Game {i+1}", key=f"rent_title_{i}")
        with col_rate:
            daily_rate = st.number_input(f"ราคา/วัน (>=0)", min_value=0.0, value=50.0, key=f"rent_rate_{i}")
        with col_days:
            rental_days = st.number_input(f"จำนวนวัน (>0)", min_value=1, value=1, step=1, key=f"rent_days_{i}")
        
        item_total = daily_rate * rental_days
        subtotal += item_total

# CASE 3: Game Return Service
elif service_type == 3:
    st.markdown("#### 🔄 CASE 3: Game Return Service (คืนเกม / คำนวณค่าปรับ 🧸)")
    num_items = st.number_input("🧩 จำนวนเกมที่นำมาคืน (total games):", min_value=1, value=1, step=1)
    
    subtotal = 0.0
    for i in range(int(num_items)):
        st.markdown(f"**🎈 รายการเกมที่ #{i+1}**")
        col_name, col_days = st.columns([2, 2])
        with col_name:
            game_name = st.text_input(f"ชื่อเกม #{i+1}", value=f"Board Game {i+1}", key=f"return_title_{i}")
        with col_days:
            late_days = st.number_input(f"ส่งเกินกำหนด/วัน (late days >= 0)", min_value=0, value=0, step=1, key=f"return_late_{i}")
        
        item_fee = late_days * LATE_FEE_RATE
        subtotal += float(item_fee)

# ==========================================
# DISCOUNT AND VAT CALCULATION
# ==========================================
st.markdown("<hr style='border: 1px dashed #b8e2f2;'>", unsafe_allow_html=True)
if service_type in [1, 2]:
    st.markdown("### 👑 สิทธิประโยชน์สมาชิก (Member Discount)")
    is_member = st.checkbox("💖 เป็นสมาชิกของร้าน (รับส่วนลดพิเศษ 10%)", value=False)
    
    if is_member:
        discount = subtotal * MEMBER_DISCOUNT
    else:
        discount = 0.0
        
    total_after_discount = subtotal - discount
    vat = total_after_discount * VAT_RATE
    net_total = total_after_discount + vat

elif service_type == 3:
    discount = 0.0
    vat = 0.0
    net_total = subtotal

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# OUTPUT RECEIPT GENERATION
# ==========================================
if st.button("💐 PRINT RECEIPT / คำนวณและออกใบเสร็จ 🧾", type="primary", use_container_width=True):
    st.markdown("<h3 style='text-align: center; color: #4a90e2;'>🧾 สรุปใบเสร็จรับเงิน (Receipt) 🧾</h3>", unsafe_allow_html=True)
    
    st.code(f"""
========================================
       🧃 GAME SHOP RECEIPT 🧸        
========================================
Customer Name : {customer_name}
Service Type  : {service_type}
----------------------------------------
""", language="text")

    if service_type in [1, 2]:
        st.code(f"""Subtotal            : {subtotal:,.2f} THB
Member Discount(10%): -{discount:,.2f} THB
VAT (7%)            : +{vat:,.2f} THB
----------------------------------------