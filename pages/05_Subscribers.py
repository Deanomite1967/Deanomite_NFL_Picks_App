import streamlit as st
import subscribers   # THIS is the fix

st.set_page_config(page_title="Subscribers", page_icon="📬", layout="wide")
st.title("📬 Subscriber Management")

st.write("Subscribers will periodically receive updates from Deanomite regarding pick selections and the process.")

new_email = st.text_input("Email")

if st.button("Add Subscriber"):
    subscribers.add_subscriber(new_email.strip())
    st.success(f"{new_email} added.")

if st.button("Remove Subscriber"):
    subscribers.remove_subscriber(new_email.strip())
    st.success(f"{new_email} removed.")



st.markdown(
    """
    <a href="mailto:kydeano28@yahoo.com" style="text-decoration:none;">
        <button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
            Email Deanomite with questions or suggestions
        </button>
    </a>
    """,
    unsafe_allow_html=True
)


