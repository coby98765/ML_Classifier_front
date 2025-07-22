import os
import streamlit as st
import requests

API_URL = os.getenv("BACKEND_URL", "http://localhost:8001")  # fallback

st.set_page_config(page_title="Classify Sample", page_icon="🔍")

st.title("🔍 Classify Sample with Trained Model")

# Step 1: Fetch available models
with st.spinner("⏳ Fetching models..."):
    try:
        data = requests.get(f"{API_URL}/models", timeout=10).json()
        models = data["models"]
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        models = []

if not models:
    st.warning("No models available. Please train one first.")
    st.stop()

# Step 2: Choose model
model_options = ["--"] + models
selected_model = st.selectbox("Select a model", model_options)

if selected_model == "--":
    st.info("Please select a trained model to continue.")
    st.stop()

# Step 3: Fetch model architecture
with st.spinner("⏳ Fetching model architecture..."):
    try:
        res = requests.get(f"{API_URL}/models/{selected_model}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            architecture = data["arc"]
        else:
            st.error(f"Failed to fetch architecture: {res.status_code}")
            st.stop()
    except Exception as e:
        st.error(f"Failed to fetch model architecture: {e}")
        st.stop()

# Step 4: Dynamically build form based on features
st.subheader("📥 Input Features")
with st.form("classify_form"):
    user_input = {}
    for feature, options in architecture.items():
        user_input[feature] = st.selectbox(f"{feature}", options)

    submitted = st.form_submit_button("Classify")

if submitted:
    with st.spinner("🔍 Classifying..."):
        try:
            response = requests.post(
                f"{API_URL}/classify/{selected_model}",
                json=user_input,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                st.success(f"🧾 Result: **{data['result']}**")
                st.markdown("### 🔢 Confidence Breakdown")
                for k, v in data["rate"].items():
                    st.markdown(f"- `{k}` → **{v:.2f}%**")
                st.markdown(f"### 🎯 Model Accuracy: `{data['accuracy']}`")

            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
