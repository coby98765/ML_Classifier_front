import os
import streamlit as st
import requests

API_URL = os.getenv("BACKEND_URL", "http://localhost:8001")  # fallback

st.set_page_config(page_title="Classify Sample", page_icon="🔍")

st.title("🔍 Classify Sample with Trained Model")

# ✅ Cache model list
@st.cache_data(ttl=60)
def fetch_model_list():
    model_list_res = requests.get(f"{API_URL}/models").json()
    return model_list_res['models']

# ✅ Cache arc per model
@st.cache_data(ttl=60)
def fetch_model_arc(model_name):
    model_arc_res = requests.get(f"{API_URL}/models/{model_name}")
    return model_arc_res.json()["arc"]


# Step 1: Fetch available models
with st.spinner("⏳ Fetching models..."):
    try:
        models = fetch_model_list()
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


if selected_model != "--":
    # Step 3: Fetch model architecture
    with st.spinner("⏳ Fetching model architecture..."):
        try:
            if "arc" not in st.session_state or st.session_state.get("model_loaded") != selected_model:
                st.session_state["arc"] = fetch_model_arc(selected_model)
                st.session_state["model_loaded"] = selected_model
        except Exception as e:
            st.error(f"Failed to fetch model architecture: {e}")
            st.stop()

    arc = st.session_state["arc"]

    # Step 4: Dynamically build form based on features
    st.subheader("📥 Input Features")
    with st.form("classify_form"):
        user_input = {}
        for feature, options in arc.items():
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
                    st.markdown(f"### 🎯 Model Accuracy: `{data['accuracy']}%`")

                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
