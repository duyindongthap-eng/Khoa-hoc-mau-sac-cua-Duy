import streamlit as st

st.header("Kiểm Tra Độ Tương Phản Màu Sắc Theo Chuẩn WCAG")
st.write("Trong khoa học màu sắc, sự phối hợp giữa màu chữ và màu nền cần đảm bảo tỷ lệ tương phản độ sáng (Contrast Ratio) đạt chuẩn quốc tế để tối ưu hóa thị giác người nhìn.")

#  Khu vực chọn màu tương tác bằng Color Picker
col_picker1, col_picker2 = st.columns(2)
with col_picker1:
    text_hex = st.color_picker("Chọn Màu Chữ (Text Color):","#FFFFFF")
with col_picker2:
    bg_hex = st.color_picker("Chọn Màu Nền (Background Color):""#1A4A7C")

# Hàm toán học tính Độ sáng tương đối (Relative Luminance) chuẩn CIE 1931
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    # Chuẩn hóa giá trị về khoảng 0.0 - 1.0
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Áp dụng công thức hiệu chỉnh Gamma tuyến tính hóa sRGB sang XYZ
    r_linear = r_norm / 12.92 if r_norm <= 0.03928 else ((r_norm + 0.055) / 1.055) ** 2.4
    g_linear = g_norm / 12.92 if g_norm <= 0.03928 else ((g_norm + 0.055) / 1.055) ** 2.4
    b_linear = b_norm / 12.92 if b_norm <= 0.03928 else ((b_norm + 0.055) / 1.055) ** 2.4
    
    # Công thức tính độ sáng Y của không gian màu CIE XYZ
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

# Tính độ sáng của chữ và nền
lum_text = get_luminance(text_hex)
lum_bg = get_luminance(bg_hex)

# Tính tỷ lệ tương phản (Contrast Ratio) theo công thức WCAG: (L1 + 0.05) / (L2 + 0.05)
l1 = max(lum_text, lum_bg)
l2 = min(lum_text, lum_bg)
contrast_ratio = (l1 + 0.05) / (l2 + 0.05)

# Hiển thị bảng xem trước (Preview) trực quan cho thầy chấm điểm
st.subheader("Bản xem trước giao diện thực tế")
st.markdown(
    f"""
    <div style="
        background-color: {bg_hex}; 
        color: {text_hex}; 
        padding: 25px; 
        border-radius: 8px; 
        text-align: center;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    ">
        <h3 style="color: {text_hex}; margin: 0; font-size: 24px; font-weight: bold;">Trường Đại học Công nghệ Kỹ thuật TP.HCM</h3>
        <p style="margin: 10px 0 0 0; font-size: 16px;">Nguyễn Quốc Duy - MSV: 23458007. 
        (Dòng chữ này đang mô phỏng tỷ lệ tương phản thực tế giữa màu chữ và nền bạn đã chọn.)</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 5. Đánh giá và xếp hạng theo tiêu chuẩn quốc tế WCAG
st.subheader("Kết quả phân tích chỉ số")
st.metric(label="Tỷ lệ tương phản đạt được (Contrast Ratio):", value=f"{contrast_ratio:.2f} : 1")

# Đánh giá theo các cấp độ tiêu chuẩn AA và AAA
pass_aa_normal = contrast_ratio >= 4.5
pass_aaa_normal = contrast_ratio >= 7.0

col_aa, col_aaa = st.columns(2)
with col_aa:
    if pass_aa_normal:
        st.success("Đạt chuẩn AA (Tỷ lệ >= 4.5:1)\nChữ hiển thị rõ ràng, dễ đọc đối với hầu hết mọi người.")
    else:
        st.error("Không đạt chuẩn AA (Tỷ lệ < 4.5:1)\nChữ quá mờ, gây mỏi mắt và khó đọc.")

with col_aaa:
    if pass_aaa_normal:
        st.success("Đạt chuẩn cao cấp AAA (Tỷ lệ >= 7.0:1)\nĐộ tương phản xuất sắc, cực kỳ sắc nét kể cả với người mắt kém.")
    else:
        st.warning("Chưa đạt chuẩn AAA (Tỷ lệ < 7.0:1)\nMàu sắc phối hợp ở mức chấp nhận được nhưng chưa đạt độ tương phản tối đa.")
