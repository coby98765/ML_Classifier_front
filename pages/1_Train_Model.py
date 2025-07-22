import os
import streamlit as st
import requests

API_URL = os.getenv("BACKEND_URL", "http://localhost:8001")  # fallback default

st.set_page_config(page_title="Train Model", page_icon="🧠")

st.title("🧠 Train a New Model")

with st.form("train_form"):
    model_name = st.text_input("Model Name")
    csv_url = st.text_input("CSV File URL")
    submitted = st.form_submit_button("Train Model")

    if submitted:
        if not model_name or not csv_url:
            st.warning("Please fill in both fields.")
        else:
            payload = {"name": model_name, "file": csv_url}
            with st.spinner("⏳ Training model..."):
                try:
                    res = requests.post(f"{API_URL}/train", json=payload, timeout=30)
                    if res.status_code == 200:
                        data = res.json()
                        print(data)
                        st.success(f"✅ Model '{data['model']}' trained with {data['accuracy']:.2f}% accuracy.")
                    else:
                        st.error(f"❌ Error: {res.status_code} - {res.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Request failed: {e}")
