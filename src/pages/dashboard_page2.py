import streamlit as st

def colored_metric(label, value, color):
    st.markdown(f"""
        <div style="
            padding:12px 16px;
            border-radius:10px;
            background-color:#f8f9fa;
            border:1px solid #eee;
            display:inline-block;
            text-align:center;
            width:100%;
        ">
            <div style="font-size:20px;  opacity:1;">
                {label}
            </div>
            <div style="font-size:48px; font-weight:700; color:{color}; margin-top:4px;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)





def run(ui):




    st.subheader("📊 Processing Dashboard")
    #ui = StreamlitUI()
    # -------------------------
    # Check if metrics exist
    # -------------------------
    if "metrics" not in st.session_state or not st.session_state.metrics:
        ui.warning("No metrics available yet. Please upload and process JPG files first.")
        st.stop()

    m = st.session_state.metrics

    # -------------------------
    # Top-Level Metrics
    # -------------------------


    col1, col2, col3 = st.columns(3)

    with col1:
        colored_metric("Total Documents", m["total_docs"], "#0ea5e9")

    with col2:
        colored_metric("Correct Classification", m["correct_classification"], "#16a34a")

    with col3:
        colored_metric("Incorrect Classification", m["incorrect_classification"], "#dc2626")





    col4, col5, col6 = st.columns(3)

    with col4:
        colored_metric("LLM Failures", m["llm_failures"],  "#dc2626")
    with col5:
        colored_metric("Correct Predictions", m["correct_predictions"], "#16a34a")
    with col6:
        colored_metric("Incorrect Predictions", m["incorrect_predictions"], "#dc2626")

    processing_times = m["processing_times"]
    avg_time = round(sum(processing_times) / len(processing_times), 2) if processing_times else 0

    accuracy = m["accuracy"]
    avg_accuracy = round(sum(accuracy) / len(accuracy), 2)*100 if accuracy else 0


    col7, col8, _ = st.columns(3)
    with col7:
        colored_metric("Avg Processing Time (sec)", avg_time, "#0ea5e9")
    with col8:
        colored_metric("Avg Accuracy %", avg_accuracy, "#0ea5e9")
    # st.subheader("Raw Metrics Data")
    # #st.dataframe(m.to_dict())  # Use to_dict() to convert to dataframe-friendly dict


    # -------------------------
    # Raw Metrics Data
    # -------------------------
    # st.subheader("Raw Metrics Data")
    # st.dataframe(m)
