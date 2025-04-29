import streamlit as st
import requests
import os

# App Configuration
st.set_page_config(page_title="Stress Detector", layout="centered")

# ---- Custom CSS Styling for Clean and Simple UI ----
st.markdown("""
    <style>
    /* Set the gradient background for the whole page */
    body {
        background: linear-gradient(45deg, #FF80A0, #FFB74D); /* Pink to Orange gradient */
        color: #fff; /* White text for contrast */
        margin: 0;
        padding: 0;
        font-family: 'Arial', sans-serif; /* Simple font */
    }
    
    /* Container for the content */
    .stApp {
        background-color: #ffffff; /* White background for content area */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Soft shadow for modern look */
        max-width: 500px;
        margin: auto;
        margin-top: 80px; /* Space at the top */
    }
    
    /* Headings */
    h1, h2 {
        text-align: center;
        color: #333;
        font-weight: bold;
    }

    /* Style for input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #f9f9f9; /* Light gray input fields */
        border: 1px solid #ddd; /* Soft border */
        color: #333;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 16px;
    }
    
    /* Style for submit button */
    button[kind="primary"] {
        background-color: #FF80A0; /* Light pink for the button */
        color: white;
        border-radius: 8px;
        padding: 1rem;
        width: 100%;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    
    button[kind="primary"]:hover {
        background-color: #FF607D; /* Darker pink for hover effect */
    }

    /* Style for labels */
    .stTextInput>label, .stNumberInput>label {
        font-size: 14px;
        color: #333;
    }
    
    /* Style for success message */
    .stSuccess {
        background-color: #00C7B7;
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Error message style */
    .stError {
        background-color: #f44336;
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("Stress Level Detector")
st.subheader("Enter your daily metrics below:")

# ---- Stress Detection Form ----
def detect_stress():
    with st.form(key="stress_form"):
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
        temperature = st.number_input("Temperature (°F)", min_value=60.0, max_value=120.0, step=0.1)
        step_count = st.number_input("Step Count", min_value=0, max_value=50000, step=1)
        submit = st.form_submit_button("Predict Stress Level")

    if submit:
        payload = {
            "humidity": humidity,
            "temperature": temperature,
            "step_count": step_count
        }

        try:
            response = requests.post("http://127.0.0.1:5050/predict", json=payload)
            result = response.json()

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                code = result["stress_level_code"]
                label = result["stress_level_label"]
                st.success(f"Predicted Stress Level: {label} (Code: {code})")

        except Exception as e:
            st.error("Could not connect to the prediction server.")
            st.error(f"Details: {e}")

# ---- Show README Functionality ----
def show_readme():
    readme_path = "README.md"  # Specify the relative path to your README file here
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding='utf-8') as file:
            readme_content = file.read()
        st.markdown("### Project README")
        st.markdown(f"```\n{readme_content}\n```")
    else:
        st.error("README file not found.")

# ---- Sidebar with Navigation ----
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Detect Stress", "View README"])

# Show Content Based on Selection
if selection == "Detect Stress":
    detect_stress()
elif selection == "View README":
    show_readme()
