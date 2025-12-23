import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Cấu hình trang Web
st.set_page_config(page_title="Dashboard Phân Tích Dữ Liệu", layout="wide")

# Tiêu đề chính
st.title("📂 Web App Phân Tích Dữ Liệu Excel/CSV")
st.markdown("---")

# 2. KHUVỰC UPLOAD FILE (SIDEBAR)
with st.sidebar:
    st.header("1. Nhập liệu")
    uploaded_file = st.file_uploader("Kéo thả file Excel/CSV vào đây:", type=['xlsx', 'xls', 'csv'])
    
    # Thêm tùy chọn số dòng cần bỏ qua (Header)
    # Mặc định để 13 vì file cũ của bạn có 13 dòng thừa
    skip_rows = st.number_input("Số dòng tiêu đề cần bỏ qua (Header):", min_value=0, value=13, step=1)
    
    st.info("Mẹo: Nếu bảng dữ liệu bị lỗi tiêu đề, hãy điều chỉnh số dòng bỏ qua ở trên.")

# 3. Xử lý dữ liệu khi có file
if uploaded_file is not None:
    try:
        # Kiểm tra đuôi file để chọn cách đọc phù hợp
        file_name = uploaded_file.name
        if file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, skiprows=skip_rows)
        else:
            # Cần cài thêm thư viện openpyxl nếu chưa có: pip install openpyxl
            df = pd.read_excel(uploaded_file, skiprows=skip_rows)

        # Xử lý sơ bộ: Xóa cột/dòng hoàn toàn rỗng
        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)

        # --- GIAO DIỆN DASHBOARD ---
        
        # Hiển thị dữ liệu thô (để kiểm tra)
        with st.expander("👀 Xem dữ liệu gốc (Click để mở rộng)"):
            st.dataframe(df)

        # Tách cột Số và cột Chữ tự động
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        obj_cols = df.select_dtypes(include=['object']).columns.tolist()

        if not num_cols:
            st.error("Lỗi: Không tìm thấy cột số liệu nào để vẽ biểu đồ! Hãy kiểm tra lại số dòng tiêu đề cần bỏ qua.")
        else:
            # 4. Khu vực Biểu đồ & Chỉ số
            st.header("2. Phân tích")
            
            # Hàng 1: Các chỉ số tổng quan (KPI)
            cols = st.columns(4)
            for i, col_name in enumerate(num_cols[:4]): # Lấy tối đa 4 cột số đầu tiên
                total = df[col_name].sum()
                with cols[i]:
                    st.metric(label=f"Tổng {col_name}", value=f"{total:,.0f}")

            st.markdown("---")

            # Hàng 2: Vẽ biểu đồ tùy chỉnh
            c1, c2 = st.columns([1, 3])
            
            with c1:
                st.subheader("Tùy chỉnh biểu đồ")
                if obj_cols:
                    x_axis = st.selectbox("Chọn trục X (Phân loại):", obj_cols)
                else:
                    x_axis = st.selectbox("Chọn trục X:", df.columns)
                    
                y_axis = st.selectbox("Chọn trục Y (Giá trị):", num_cols)
                chart_type = st.radio("Loại biểu đồ:", ["Cột (Bar)", "Đường (Line)", "Tròn (Pie)"])

            with c2:
                if chart_type == "Cột (Bar)":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"Biểu đồ cột: {y_axis} theo {x_axis}", text_auto='.2s')
                elif chart_type == "Đường (Line)":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"Xu hướng: {y_axis}")
                elif chart_type == "Tròn (Pie)":
                    fig = px.pie(df, names=x_axis, values=y_axis, title=f"Tỷ trọng {y_axis} theo {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Có lỗi khi đọc file: {e}")
        st.warning("Gợi ý: Hãy thử tăng/giảm 'Số dòng tiêu đề cần bỏ qua' ở cột bên trái.")

else:
    # Màn hình chờ khi chưa upload file
    st.info("👋 Chào bạn! Vui lòng tải file báo cáo (.xls, .xlsx, .csv) lên từ thanh bên trái để bắt đầu phân tích.
