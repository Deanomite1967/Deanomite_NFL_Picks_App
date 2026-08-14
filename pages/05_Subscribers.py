import streamlit as st
import subscribers

st.set_page_config(page_title="Subscribers", page_icon="📬", layout="wide")
st.title("📬 Subscriber Management")

# Initialize DB only after Streamlit is ready
if st.session_state.get("db_initialized") is None:
    subscribers.init_db()
    st.session_state["db_initialized"] = True

st.write("Subscribers will periodically receive updates from Deanomite regarding pick selections and the process.")


# -----------------------------------------
# Add subscriber
# -----------------------------------------
st.subheader("Add Subscriber")

new_email = st.text_input("Email address to subscribe")

if st.button("Subscribe"):
    if new_email.strip() == "":
        st.warning("Please enter an email.")
    else:
        success = add_subscriber(new_email.strip())
        if success:
            st.success(f"{new_email} subscribed successfully.")
        else:
            st.info(f"{new_email} is already subscribed.")

# -----------------------------------------
# Remove subscriber
# -----------------------------------------
st.subheader("Remove Subscriber")

remove_email = st.text_input("Email address to unsubscribe")

if st.button("Unsubscribe"):
    if remove_email.strip() == "":
        st.warning("Please enter an email.")
    else:
        remove_subscriber(remove_email.strip())
        st.success(f"{remove_email} unsubscribed successfully.")
        

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


