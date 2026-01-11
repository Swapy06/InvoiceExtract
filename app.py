import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Function to load Gemini Pro Vision model and get responses
def get_gemini_response(input_prompt, image_data, user_prompt):
    # 'gemini-1.5-flash' is excellent for document understanding and faster/cheaper than Pro
    # You can also use 'gemini-1.5-pro' for higher reasoning capabilities
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image_data[0], user_prompt])
    return response.text

# 3. Function to prepare the image for the API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# 4. Streamlit App UI Setup
st.set_page_config(page_title="Multi-Language Invoice Extractor")

st.header("Multi-Language Invoice Extractor 🤖")
st.subheader("Powered by Google Gemini")

# User Inputs
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice.", use_column_width=True)

submit = st.button("Tell me about the invoice")

# 5. The System Prompt (Instructions for the AI)
input_system_prompt = """
You are an expert in understanding invoices.
You will receive input images as invoices and
you will have to answer questions based on the input image.
"""

# 6. Handling the Submit Action
if submit:
    if uploaded_file is None:
        st.warning("Please upload an invoice image first.")
    else:
        with st.spinner("Analyzing Invoice..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_system_prompt, image_data, input_prompt)
                
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")