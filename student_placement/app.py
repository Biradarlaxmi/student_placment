import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------- Custom Page Config ----------
st.set_page_config(
    page_title="🌐 User Info Dashboard",
    layout="wide",
    page_icon="📋"
)

# ---------- Custom CSS Styling ----------
custom_css = """
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(to right, #e0eafc, #cfdef3);
    font-family: 'Segoe UI', sans-serif;
}

/* Title styling */
h1 {
    color: #1f4e79;
    text-align: center;
}

/* Footer */
footer {
    visibility: hidden;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- DB Functions ----------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS user_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )''')
    conn.commit()

def insert_user(name, email, age):
    try:
        c.execute("INSERT INTO user_info (name, email, age) VALUES (?, ?, ?)", (name, email, age))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_users():
    c.execute("SELECT * FROM user_info")
    return c.fetchall()

# ---------- UI Content ----------
create_table()

st.markdown("## 👤 Welcome to the User Information Dashboard")

# --- Input Form ---
with st.expander("➕ Add New User", expanded=True):
    with st.form("user_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Enter your Name")
        with col2:
            email = st.text_input("📧 Enter your Email")
        age = st.slider("🎂 Select your Age", min_value=1, max_value=120, value=25)
        submitted = st.form_submit_button("🚀 Submit")

        if submitted:
            if name and email:
                if insert_user(name, email, age):
                    st.success("✅ User added successfully!")
                else:
                    st.error("⚠️ Email already exists.")
            else:
                st.warning("❗ Name and Email are required.")

# --- Fetch Data ---
user_data = get_all_users()
df = pd.DataFrame(user_data, columns=["ID", "Name", "Email", "Age"])

# --- Stats Cards ---
st.markdown("### 📈 Live Summary Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="👥 Total Users", value=len(df))
with col2:
    st.metric(label="🔢 Average Age", value=int(df['Age'].mean()) if not df.empty else 0)
with col3:
    st.metric(label="🧓 Max Age", value=int(df['Age'].max()) if not df.empty else 0)

# --- User Table Display ---
st.markdown("### 📋 Registered User Data")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No users found. Please add some users to populate data.")

# --- Age Distribution Chart ---
if not df.empty:
    st.markdown("### 📊 Age Distribution of Users")
    fig = px.histogram(df, x="Age", nbins=10, title="User Age Histogram",
                       color_discrete_sequence=["#007FFF"])
    fig.update_layout(bargap=0.2, xaxis_title="Age", yaxis_title="Count", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("<center>Made with ❤️ using Streamlit • [GitHub](https://github.com)</center>", unsafe_allow_html=True)
