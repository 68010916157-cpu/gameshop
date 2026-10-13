import streamlit as st
import pandas as pd
from datetime import datetime

# ตั้งค่าหน้าตาเบื้องต้น
st.set_page_config(page_title="Board Game Cafe System", page_icon="🎲", layout="wide")

st.title("🎲 ระบบจัดการร้านบอร์ดเกม (Board Game Cafe)")
st.caption("ระบบบริการเล่นในร้าน เช่า-คืนเกม และคำนวณส่วนลดพร้อมภาษี VAT 7%")

# ข้อมูลเกมตัวอย่าง
if 'games' not in st.state_state:
    st.session_state['games'] = [
        {"id": 101, "name": "Catan", "rate_per_day": 50, "stock": 3},
        {"id": 102, "name": "Codenames", "rate_per_day": 30, "stock": 5},
        {"id": 103, "name": "Splendor", "rate_per_day": 40, "stock": 2},
        {"id": 104, "name": "Avalon", "rate_per_day": 35, "stock": 4},
        {"id": 105, "name": "Dixit", "rate_per_day": 45, "stock": 3},
    ]

# ข้อมูลตารางการใช้บริการในร้าน/เช่า
if 'rentals' not in st.session_state:
    st.session_state['rentals'] = []

tab1, tab2, tab3 = st.tabs(["🎮 บริการเล่นในร้าน / เช่าเกม", "🔄 คืนเกม", "📊 รายการธุรกรรม"])

# --- TAB 1: เช่า / เล่นในร้าน ---
with tab1:
    st.header("ทำรายการเช่า หรือ นั่งเล่นในร้าน")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        customer_name = st.text_input("ชื่อลูกค้า", value="ลูกค้าทั่วไป")
        service_type = st.radio("ประเภทบริการ", ["เล่นในร้าน (In-Store Play)", "เช่ากลับบ้าน (Rental)"])
        is_member = st.checkbox("เป็นสมาชิก (ส่วนลด 10%)")
        
    with col2:
        df_games = pd.DataFrame(st.session_state['games'])
        selected_game_names = st.multiselect(
            "เลือกบอร์ดเกมที่ต้องการ (เลือกได้หลายรายการ)", 
            options=df_games['name'].tolist()
        )
        
        hours_or_days = st.number_input(
            "จำนวนชั่วโมง (กรณีเล่นในร้าน) / จำนวนวัน (กรณีเช่ากลับบ้าน)", 
            min_value=1, value=1, step=1
        )

    if st.button("คำนวณและบันทึกรายการ", type="primary"):
        if not selected_game_names:
            st.error("กรุณาเลือกเกมอย่างน้อย 1 รายการ")
        else:
            selected_games = df_games[df_games['name'].isin(selected_game_names)]
            
            # คำนวณราคาพื้นฐาน
            if service_type == "เล่นในร้าน (In-Store Play)":
                base_rate = 40  # ค่าบริการเล่นในร้าน 40 บาท/ชั่วโมง/คน
                subtotal = base_rate * hours_or_days * len(selected_game_names)
            else:
                subtotal = selected_games['rate_per_day'].sum() * hours_or_days
            
            # ส่วนลดสมาชิก
            discount = subtotal * 0.10 if is_member else 0.0
            price_after_discount = subtotal - discount
            
            # คำนวณ VAT 7%
            vat = price_after_discount * 0.07
            total_amount = price_after_discount + vat
            
            st.success("บันทึกรายการเรียบร้อย!")
            
            # แสดงใบเสร็จ/สรุปยอด
            st.subheader("🧾 สรุปยอดชำระเงิน")
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.write(f"**ลูกค้า:** {customer_name}")
                st.write(f"**รายการเกม:** {', '.join(selected_game_names)}")
                st.write(f"**ประเภท:** {service_type}")
            with res_col2:
                st.write(f"ยอดรวมก่อนส่วนลด: {subtotal:,.2f} บาท")
                st.write(f"ส่วนลดสมาชิก (10%): -{discount:,.2f} บาท")
                st.write(f"ภาษีมูลค่าเพิ่ม (VAT 7%): +{vat:,.2f} บาท")
                st.markdown(f"### **ยอดชำระสุทธิ: {total_amount:,.2f} บาท**")
            
            # บันทึกข้อมูล
            st.session_state['rentals'].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "customer": customer_name,
                "type": service_type,
                "items": ", ".join(selected_game_names),
                "total": total_amount,
                "status": "กำลังใช้งาน/เช่าอยู่"
            })

# --- TAB 2: คืนเกม ---
with tab2:
    st.header("ทำรายการคืนเกม")
    if len(st.session_state['rentals']) == 0:
        st.info("ยังไม่มีรายการเช่าในระบบ")
    else:
        active_rentals = [r for r in st.session_state['rentals'] if r['status'] == "กำลังใช้งาน/เช่าอยู่"]
        if not active_rentals:
            st.info("ไม่มีรายการที่ค้างคืนอยู่")
        else:
            rental_options = [f"{r['customer']} - {r['items']} ({r['time']})" for r in active_rentals]
            selected_return = st.selectbox("เลือกรายการที่ต้องการคืน", options=rental_options)
            
            if st.button("ยืนยันการรับคืน"):
                for r in st.session_state['rentals']:
                    if f"{r['customer']} - {r['items']} ({r['time']})" == selected_return:
                        r['status'] = "คืนเรียบร้อยแล้ว"
                        break
                st.success("รับคืนรายการสำเร็จ!")
                st.rerun()

# --- TAB 3: รายการธุรกรรมทั้งหมด ---
with tab3:
    st.header("ประวัติการทำรายการ")
    if len(st.session_state['rentals']) > 0:
        df_log = pd.DataFrame(st.session_state['rentals'])
        st.dataframe(df_log, use_container_width=True)
    else:
        st.write("ยังไม่มีข้อมูลธุรกรรม")