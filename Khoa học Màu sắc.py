import streamlit as st

st.set_page_config(
    page_title="Khoa học Màu sắc", layout="wide"
)

col_logo_truong, col_text, col_logo_khoa = st.columns([1.5, 5, 1.5])

with col_logo_truong:
    # Logo trường nằm bên góc trái hàng ngang
    st.image("Logo_HCMUTE.png", width=120)

with col_text:
    # Khối chữ tên Trường và Khoa nằm ở chính giữa hàng ngang, tự động căn giữa dọc tâm với logo
    st.markdown(
        """
        <div style="
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            height: 140px; 
            text-align: center;
        ">
            <h3 style="color: #1a4a7c; margin: 0; font-weight: bold; font-size: 24px; font-family: 'Segoe UI', Arial, sans-serif;">
                TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT THÀNH PHỐ HỒ CHÍ MINH
            </h3>
            <h3 style="color: #475569; margin: 10px 0 0 0; font-weight: 600; font-size: 20px; font-family: 'Segoe UI', Arial, sans-serif;">
                KHOA MỸ THUẬT VÀ TRUYỀN THÔNG
            </h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col_logo_khoa:
    # Logo khoa nằm bên góc phải hàng ngang (Cùng hàng với logo trường)
    st.image("logo_khoa.png", width=140)

# Đường kẻ phân cách
st.markdown("<hr style='margin-top: 15px; margin-bottom: 25px; border: 1px solid #eee;'>", unsafe_allow_html=True)

st.write("### Chào mừng bạn đến với project Khoa học Màu sắc của mình!")
st.write("# Mình tên là Nguyễn Quốc Duy, MSV: 23458007")
