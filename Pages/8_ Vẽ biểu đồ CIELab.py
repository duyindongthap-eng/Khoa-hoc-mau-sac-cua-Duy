import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import colour

# Tiêu đề bài tập
st.markdown("<h3 style='text-align: center; color: #1a4a7c;'>MÔ PHỎNG SỰ DỊCH CHUYỂN MÀU CIELAB</h3>", unsafe_allow_html=True)
st.write("Ứng dụng cấu trúc không gian màu độc lập thiết bị CIELAB dựa trên tài liệu chuẩn của X-Rite để phân tích sự dịch chuyển sắc độ.")

# ---------------------------------------------------------
# 1. KHU VỰC NHẬP DỮ LIỆU TƯƠNG TÁC
# ---------------------------------------------------------
st.subheader("Nhập tọa độ màu Lab1 và Lab2")
col_input1, col_input2 = st.columns(2)

with col_input1:
    st.markdown("#### Màu xuất phát ($Lab_1$)")
    l1 = st.number_input("L1* (Độ sáng: 0 → 100)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    a1 = st.number_input("a1* (Trục Lá/Đỏ: -128 → 128)", min_value=-128.0, max_value=128.0, value=-25.0, step=1.0)
    b1 = st.number_input("b1* (Trục Dương/Vàng: -128 → 128)", min_value=-128.0, max_value=128.0, value=35.0, step=1.0)

with col_input2:
    st.markdown("#### Màu đích đến ($Lab_2$)")
    l2 = st.number_input("L2* (Độ sáng: 0 → 100)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
    a2 = st.number_input("a2* (Trục Lá/Đỏ: -128 → 128)", min_value=-128.0, max_value=128.0, value=40.0, step=1.0)
    b2 = st.number_input("b2* (Trục Dương/Vàng: -128 → 128)", min_value=-128.0, max_value=128.0, value=-15.0, step=1.0)

Lab1 = np.array([l1, a1, b1])
Lab2 = np.array([l2, a2, b2])

# ---------------------------------------------------------
# 2. CHUYỂN ĐỔI TOÁN HỌC SANG RGB ĐỂ HIỂN THỊ MÀU THỰC TẾ
# ---------------------------------------------------------
def lab_to_hex(Lab):
    # Chuyển đổi thông qua không gian XYZ tiêu chuẩn với nguồn sáng D65
    XYZ = colour.Lab_to_XYZ(Lab)
    sRGB = colour.XYZ_to_sRGB(XYZ)
    # Giới hạn mảng để tránh lỗi tràn màu khi tính toán hình ảnh
    sRGB_clipped = np.clip(sRGB, 0, 1)
    return '#{:02x}{:02x}{:02x}'.format(int(sRGB_clipped[0]*255), int(sRGB_clipped[1]*255), int(sRGB_clipped[2]*255))

hex1 = lab_to_hex(Lab1)
hex2 = lab_to_hex(Lab2)

# Tính toán khoảng cách lệch màu tổng thể Delta E (CIE 1976)
delta_E = np.sqrt((l2 - l1)**2 + (a2 - a1)**2 + (b2 - b1)**2)

# ---------------------------------------------------------
# 3. TIẾN HÀNH VẼ ĐỒ THỊ MẶT PHẲNG SẮC ĐỘ A* - B*
# ---------------------------------------------------------
place = st.empty()
fig, ax = plt.subplots(figsize=(6.5, 6.5))

# Vẽ đường chữ thập phân chia 4 vùng cực màu sắc độ
ax.axhline(0, color='#888888', linestyle='--', linewidth=1)
ax.axvline(0, color='#888888', linestyle='--', linewidth=1)

# Vẽ vector mũi tên dịch chuyển từ điểm 1 sang điểm 2
ax.annotate('', xy=(a2, b2), xytext=(a1, b1),
            arrowprops=dict(arrowstyle="-|>", color="#333333", lw=3, mutation_scale=20))

# Vẽ các chấm tròn hiển thị đúng màu thực tế dựa trên mã màu HEX thu được
ax.scatter(a1, b1, color=hex1, s=250, edgecolors='black', zorder=5, label='Màu đầu ($Lab_1$)')
ax.scatter(a2, b2, color=hex2, s=250, edgecolors='black', zorder=5, label='Màu cuối ($Lab_2$)')

# Đặt nhãn ký hiệu điểm tọa độ
ax.text(a1 + 4, b1 + 4, "$Lab_1$", fontsize=12, fontweight='bold', color='#1a4a7c')
ax.text(a2 + 4, b2 + 4, "$Lab_2$", fontsize=12, fontweight='bold', color='#1a4a7c')

# Thiết lập giới hạn đồ thị đối xứng theo tài liệu X-Rite
ax.set_xlim([-100, 100])
ax.set_ylim([-100, 100])

# Điền thông tin nhãn 4 hướng cực màu theo cấu trúc chuẩn của X-Rite
ax.set_xlabel('← Hướng Xanh Lá (-a*) | Trục a* | Hướng Đỏ (+a*) →', fontsize=11, fontweight='bold')
ax.set_ylabel('← Hướng Xanh Dương (-b*) | Trục b* | Hướng Vàng (+b*) →', fontsize=11, fontweight='bold')
ax.set_title('Mặt phẳng Sắc độ CIELAB ($a^* - b^*$ Diagram)', fontsize=13, fontweight='bold', pad=15)

ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='upper left')
plt.tight_layout()

# Đẩy đồ thị lên Streamlit
place.pyplot(fig, clear_figure=True)
plt.close(fig)

# ---------------------------------------------------------
# 4. KHU VỰC NHẬN XÉT TỰ ĐỘNG CHUẨN KHOA HỌC
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Nhận xét phân tích định lượng & định tính")

# Hiển thị số liệu Delta E tương tác trực quan
col_metric1, col_metric2 = st.columns(2)
with col_metric1:
    st.metric(label="Khoảng cách sai lệch màu Toán học ($\Delta E_{CIE1976}$):", value=f"{delta_E:.2f}")
with col_metric2:
    if delta_E < 1.0:
        st.success("Đánh giá: Mắt người bình thường không thể phân biệt được hai màu này (Sai số lý tưởng).")
    elif delta_E < 3.0:
        st.warning("Đánh giá: Sai lệch nhỏ, chỉ người có chuyên môn trong ngành in/nhuộm mới nhận ra.")
    else:
        st.error("Đánh giá: Hai màu sắc có sự khác biệt rất lớn, mắt thường nhìn thấy rõ rệt.")

# Thuật toán phân tích xu hướng dịch chuyển dựa trên hình học vector
nhan_xet_chi_tiet = []

# Phân tích sự thay đổi trục sáng L*
delta_L = l2 - l1
if delta_L > 5:
    nhan_xet_chi_tiet.append(f"Về độ sáng: Màu dịch chuyển sang xu hướng **Sáng hơn** (Chỉ số L* tăng {abs(delta_L):.1f} đơn vị).")
elif delta_L < -5:
    nhan_xet_chi_tiet.append(f"Về độ sáng: Màu dịch chuyển sang xu hướng **Tối đi** (Chỉ số L* giảm {abs(delta_L):.1f} đơn vị).")
else:
    nhan_xet_chi_tiet.append("Về độ sáng: Trục L* thay đổi rất ít, hai màu giữ nguyên độ tương đương về mặt ánh sáng.")

# Phân tích xu hướng biến đổi sắc độ trên hệ tọa độ vuông góc (a*, b*)
delta_a = a2 - a1
delta_b = b2 - b1

if delta_a > 10:
    nhan_xet_chi_tiet.append("Về sắc độ (Trục a*): Vector chạy sang phải, màu sắc bớt xanh lá và **tăng cường sắc Đỏ (Reddish)** rõ rệt.")
elif delta_a < -10:
    nhan_xet_chi_tiet.append("Về sắc độ (Trục a*): Vector chạy sang trái, màu sắc bớt đỏ và **tăng cường sắc Xanh Lá (Greenish)** mạnh hơn.")

if delta_b > 10:
    nhan_xet_chi_tiet.append("Về sắc độ (Trục b*): Vector hướng lên trên, màu sắc giảm xanh dương và **ngả sang tông Vàng (Yellowish)** đậm đà hơn.")
elif delta_b < -10:
    nhan_xet_chi_tiet.append("Về sắc độ (Trục b*): Vector hướng xuống dưới, màu sắc giảm vàng và **đậm đặc sắc Xanh Dương (Blueish)** sâu hơn.")

# Xuất kết luận ra màn hình
st.markdown("#### **Kết luận quỹ đạo dịch chuyển sắc độ:**")
for item in nhan_xet_chi_tiet:
    st.markdown(f" * {item}")
