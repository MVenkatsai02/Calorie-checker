import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=st.secrets["Google_api_key"])

# Function to call Gemini API
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        return None

# Streamlit UI Setup
st.set_page_config(page_title="Calorie checker", page_icon="🍎", layout="centered")

# Header Section
st.markdown(
    """
    <h1 style="text-align:center;">🍎 Calorie checker</h1>
    <p style="text-align:center; color:gray;">Analyze food items in an image and get total calorie details.</p>
    <hr>
    """, 
    unsafe_allow_html=True
)

# User Inputs
with st.container():
    st.subheader("📌 Enter Details")
    input_text = st.text_input("Enter additional context (optional):", placeholder="E.g., Is this a healthy meal?")
    uploaded_file = st.file_uploader("📷 Upload a food image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit Button
submit = st.button("🍽️ Analyze Calories", use_container_width=True)

# Define the AI Prompt
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image and calculate the total calories. 
Provide detailed calorie breakdown in the following format:

🍽️ **Calorie Breakdown**  
1. Item Name - Calories  
2. Item Name - Calories  
...
"""

# Processing and Response Display
if submit:
    if uploaded_file is None:
        st.error("⚠️ Please upload a food image before analyzing!")
    else:
        with st.spinner("Analyzing food items... 🔄"):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, input_text)

        # Display Results
        st.success("✅ Analysis Complete!")
        st.subheader("📊 Results")
        st.markdown(response, unsafe_allow_html=True)
