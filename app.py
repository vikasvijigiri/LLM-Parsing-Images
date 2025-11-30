import streamlit as st
from src.ui.streamlitUI import StreamlitUI
from src.pages import upload_page1, dashboard_page2
from src.core.state import AppState  # <-- import this

# -----------------------------
# App Setup
# -----------------------------


# # -----------------------------
# # Persistent UI object
# # -----------------------------
# if "ui" not in st.session_state:
#     st.session_state.ui = StreamlitUI()

# ui = st.session_state.ui

ui = StreamlitUI()

# -----------------------------
# Sidebar Navigation
# -----------------------------
page_choice = ui.sidebar_nav()
# -----------------------------
# Run selected page
# -----------------------------
if page_choice == "Upload & Process":
    upload_page1.run(ui)
elif page_choice == "Dashboard":
    dashboard_page2.run(ui)
