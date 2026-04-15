import streamlit as st
import pypandoc
import os

# 1. SETUP THE PAGE UI
st.set_page_config(page_title="Waleed's Document Converter", page_icon="📄", layout="centered")

# 2. SMART ENGINE SETUP (Runs once in the background)
@st.cache_resource
def setup_engine():
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()

setup_engine()

# 3. BUILD THE INTERFACE
st.title("📄 Waleed Abdullah MS Word Converter")
st.markdown("""
Welcome! Paste your AI-generated text (including math equations surrounded by `$$`) into the box below. 
Click convert, and instantly download a perfectly formatted MS Word document.
""")

# Create a clean form so the page doesn't lag while typing
with st.form("converter_form"):
    user_input = st.text_area(
        "Paste your text here:", 
        height=300, 
        placeholder="e.g., The equation for Nash-Sutcliffe Efficiency is $$NSE = 1 - ...$$"
    )
    
    # A wide, premium-looking submit button
    submitted = st.form_submit_button("⚙️ Convert to MS Word", use_container_width=True)

# 4. PROCESS THE CONVERSION
if submitted:
    if not user_input.strip():
        st.warning("⚠️ Please paste some text before converting!")
    else:
        with st.spinner("Processing your equations..."):
            try:
                # Tell Pandoc to generate the Word file
                output_file = "Final_Document.docx"
                pypandoc.convert_text(user_input, 'docx', format='md', outputfile=output_file)
                
                # Show a success message and the Download button
                st.success("✅ Conversion successful! Click below to save your file.")
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="⬇️ Download MS Word Document",
                        data=file,
                        file_name="Final_Document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
