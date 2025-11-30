import streamlit as st


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
    col1.metric("Total Documents", m["total_docs"])
    col2.metric("Correct Classification", m["correct_classification"])
    col3.metric("Incorrect Classification", m["incorrect_classification"])
    col4, col5, col6 = st.columns(3)
    col4.metric("LLM Failures", m["llm_failures"])

    col5.metric("Correct Predictions", m["correct_predictions"])
    col6.metric("Incorrect Predictions", m["incorrect_predictions"])

    processing_times = m["processing_times"]
    avg_time = round(sum(processing_times) / len(processing_times), 2) if processing_times else 0

    accuracy = m["accuracy"]
    avg_accuracy = round(sum(accuracy) / len(accuracy), 2)*100 if accuracy else 0


    col7, col8, _ = st.columns(3)
    col7.metric("Avg Processing Time (sec)", avg_time)
    col8.metric("Avg Accuracy %", avg_accuracy)
    # st.subheader("Raw Metrics Data")
    # #st.dataframe(m.to_dict())  # Use to_dict() to convert to dataframe-friendly dict


    # -------------------------
    # Raw Metrics Data
    # -------------------------
    # st.subheader("Raw Metrics Data")
    # st.dataframe(m)
