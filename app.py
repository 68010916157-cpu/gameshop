import streamlit as st

# ==========================================
# INITIALIZATION (การกำหนดค่าเริ่มต้น)
# ==========================================
IN_STORE_RATE = 50      # ค่าบริการเล่นในร้าน 50 บาท/คน/ชั่วโมง
LATE_FEE_RATE = 20      # ค่าปรับคืนเกมสาย 20 บาท/วัน/รายการ
MEMBER_DISCOUNT = 0.10  # ส่วนลดสมาชิก 10%
VAT_RATE = 0.07         # ภาษีมูลค่าเพิ่ม 7%

st.set_page_config(page_title="GAME SHOP RECEIPT", page_icon="🎲", layout="centered")

st.title("🎲 GAME SHOP MANAGEMENT SYSTEM")
st.caption("ระบบคำนวณค่าบริการ เล่นในร้าน / เช่า / คืนเกม ตามอัลกอริทึม")

# ==========================================
# USER INPUT: CUSTOMER & SERVICE SELECTION
# ==========================================
customer_name_input = st.text_input("Enter Customer Name (ชื่อลูกค้า):", value="")
customer_name = customer_name_input.strip() if customer_name_input.strip() != "" else "General Customer"

service_option = st.radio(
    "Select Service Type (เลือกประเภทบริการ):",
    ["1 = In-Store Play (เล่นในร้าน)", "2 = Game Rental Service (เช่าเกม)", "3 = Game Return Service (คืนเกม/ค่าปรับ)"]
)

# แปลงตัวเลือกเป็น service_type INTEGER (1, 2, 3)
service_type = int(service_option.split("=")[0].strip())

subtotal = 0.0
discount = 0.0
total_after_discount = 0.0
vat = 0.0
net_total = 0.0

st.markdown("---")

# ==========================================
# PROCESS SERVICE SELECTION (SWITCH service_type)
# ==========================================

# CASE 1: In-Store Play
if service_type == 1:
    st.subheader("🎮 CASE 1: In-Store Play (เล่นในร้าน)")
    col1, col2 = st.columns(2)
    with col1:
        players = st.number_input("Enter number of players (> 0):", min_value=1, value=1, step=1)
    with col2:
        hours = st.number_input("Enter hours (> 0):", min_value=1, value=1, step=1)
    
    # subtotal = players * hours * IN_STORE_RATE
    subtotal = float(players * hours * IN_STORE_RATE)

# CASE 2: Game Rental Service
elif service_type == 2:
    st.subheader("📦 CASE 2: Game Rental Service (เช่าเกม)")
    num_items = st.number_input("Enter total number of games to rent:", min_value=1, value=1, step=1)
    
    subtotal = 0.0
    for i in range(int(num_items)):
        st.markdown(f"**Game #{i+1}**")
        col_name, col_rate, col_days = st.columns([2, 1, 1])
        with col_name:
            game_name = st.text_input(f"Game Title #{i+1}", value=f"Game {i+1}", key=f"rent_title_{i}")
        with col_rate:
            daily_rate = st.number_input(f"Daily rate (>= 0)", min_value=0.0, value=50.0, key=f"rent_rate_{i}")
        with col_days:
            rental_days = st.number_input(f"Rental days (> 0)", min_value=1, value=1, step=1, key=f"rent_days_{i}")
        
        item_total = daily_rate * rental_days
        subtotal += item_total

# CASE 3: Game Return Service
elif service_type == 3:
    st.subheader("🔄 CASE 3: Game Return Service (คืนเกม)")
    num_items = st.number_input("Enter total number of games to return:", min_value=1, value=1, step=1)
    
    subtotal = 0.0
    for i in range(int(num_items)):
        st.markdown(f"**Game #{i+1}**")
        col_name, col_days = st.columns([2, 2])
        with col_name:
            game_name = st.text_input(f"Game Title #{i+1}", value=f"Game {i+1}", key=f"return_title_{i}")
        with col_days:
            late_days = st.number_input(f"Late days (>= 0)", min_value=0, value=0, step=1, key=f"return_late_{i}")
        
        item_fee = late_days * LATE_FEE_RATE
        subtotal += float(item_fee)

# ==========================================
# DISCOUNT AND VAT CALCULATION
# ==========================================
st.markdown("---")
if service_type in [1, 2]:
    is_member = st.checkbox("Is customer a member? (เป็นสมาชิกเพื่อรับส่วนลด 10%)", value=False)
    
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

# ==========================================
# OUTPUT RECEIPT GENERATION
# ==========================================
if st.button("PRINT RECEIPT / คำนวณและออกใบเสร็จ", type="primary", use_container_width=True):
    st.code(f"""
========================================
          GAME SHOP RECEIPT             
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
NET TOTAL AMOUNT    : {net_total:,.2f} THB
========================================
""", language="text")
    elif service_type == 3:
        st.code(f"""TOTAL LATE FEE      : {net_total:,.2f} THB
========================================
""", language="text")