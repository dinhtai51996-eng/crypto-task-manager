import streamlit as st
import sqlite3
import pandas as pd
import requests

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Crypto Task Manager", layout="wide")
st.title("🛡️ DINH TUAN - SUPREME COMMAND CENTER")
st.markdown("---")

# --- QUẢN LÝ DATABASE (SQLite) ---
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS my_tasks 
                 (task_name TEXT PRIMARY KEY, status TEXT)''')
    conn.commit()
    conn.close()

def mark_as_done(task_name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO my_tasks (task_name, status) VALUES (?, ?)", (task_name, 'Done'))
    conn.commit()
    conn.close()

def get_done_tasks():
    conn = sqlite3.connect('tasks.db')
    try:
        df = pd.read_sql_query("SELECT task_name FROM my_tasks", conn)
        tasks = df['task_name'].tolist()
    except:
        tasks = []
    conn.close()
    return tasks

# --- KẾT NỐI DỮ LIỆU (API) ---
def fetch_tasks_from_api():
    # Giả lập API gọi từ server
    # Trong tương lai, bạn thay URL này bằng endpoint thực tế
    return [
        "Binance: Spot Trading Volume 1000$",
        "Bybit: Join Launchpool",
        "OKX: Daily Check-in",
        "Binance: Learn & Earn New Project",
        "Bybit: Refer a Friend"
    ]

# --- CHƯƠNG TRÌNH CHÍNH ---
init_db()

# Lấy dữ liệu
all_tasks = fetch_tasks_from_api()
done_tasks = get_done_tasks()

# Chia tab hiển thị
tab1, tab2 = st.tabs(["📋 Danh sách Nhiệm vụ", "✅ Đã hoàn thành"])

with tab1:
    st.subheader("Nhiệm vụ cần thực hiện:")
    pending_tasks = [t for t in all_tasks if t not in done_tasks]
    
    if not pending_tasks:
        st.success("Tuyệt vời! Bạn đã hoàn thành tất cả nhiệm vụ.")
    else:
        for task in pending_tasks:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{task}**")
            if col2.button("Xong", key=task):
                mark_as_done(task)
                st.rerun()

with tab2:
    st.subheader("Nhiệm vụ đã hoàn thành:")
    st.write(done_tasks)
    if st.button("Reset tất cả"):
        conn = sqlite3.connect('tasks.db')
        conn.execute("DELETE FROM my_tasks")
        conn.commit()
        conn.close()
        st.rerun()

st.sidebar.info("Hệ thống quản trị cá nhân - Dinh Tuan")