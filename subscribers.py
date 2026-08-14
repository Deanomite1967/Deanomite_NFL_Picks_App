import sqlite3
import os

# -----------------------------------------
# Add subscriber
# -----------------------------------------
def add_subscriber(email):
    conn = sqlite3.connect("\pages\subscribers.db")
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO subscribers (email, date_added) VALUES (?, DATE('now'))",
            (email,)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # already subscribed
    finally:
        conn.close()

# -----------------------------------------
# Remove subscriber
# -----------------------------------------
def remove_subscriber(email):
    conn = sqlite3.connect("\pages\subscribers.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM subscribers WHERE email = ?", (email,))
    conn.commit()
    conn.close()

import streamlit as st

st.sidebar.markdown("### 📧 Contact")
st.sidebar.markdown(
    """
    <a href="mailto:kydeano28@yahoo.com" style="text-decoration:none;">
        <button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
            Email Deanomite with questions or suggestions
        </button>
    </a>
    """,
    unsafe_allow_html=True
)