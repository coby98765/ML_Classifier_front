import streamlit as st
import requests
import os

API_URL = os.getenv("BACKEND_URL", "http://localhost:8001")  # fallback default


st.set_page_config(
    page_title="Naive Bayesian Classifier",
    page_icon="👋",
)

st.title("📊 Naive Bayes Classifier")
st.markdown("Welcome! This app lets you train and test Naive Bayes models via a FastAPI backend.")

st.subheader("🔌 Backend Status")

with st.spinner("Connecting to backend..."):
    try:
        response = requests.get(f"{API_URL}/models", timeout=5)
        if response.status_code == 200:
            st.success("Backend is online and responding ✅")
            models = response.json()
            if models:
                st.markdown(f"**Available models:** `{', '.join(models['models'])}`")
            else:
                st.info("No models trained yet.")
        else:
            st.error(f"Backend responded with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Cannot connect to backend: {e}")

st.markdown("---")
st.markdown("Use the sidebar to navigate between pages:\n- **Train Model**\n- **Classify**")