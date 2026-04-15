import streamlit as st
import pypandoc
import os

# 1. SETUP THE PAGE UI
st.set_page_config(page_title="Waleed Abdullah's Document Converter", page_icon="📄", layout="centered")

# 2. SMART ENGINE SETUP
@st.cache_resource
def setup_engine():
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()

setup_engine()

# 3. BUILD THE INTERFACE
st.title("📄 Waleed's Universal Document Converter")
st.markdown("""
Welcome! Paste your AI-generated text (including math equations surrounded by `$$`) into the box below. 
Select your desired format, and instantly download your document.
""")

with st.form("converter_form"):
    user_input = st.text_area(
        "Paste your text here (Ensure a space after hashtags, e.g., '# Heading'):", 
        height=300
    )
    
    # NEW: A dictionary of all the formats Pandoc can handle
    FORMAT_OPTIONS = {
        "MS Word (.docx)": "docx",
        "PDF Document (.pdf)": "pdf",
        "HTML Webpage (.html)": "html",
        "Rich Text Format (.rtf)": "rtf",
        "E-Book (.epub)": "epub",
        "OpenDocument (.odt)": "odt",
        "LaTeX Source (.tex)": "tex"
    }
    
    # A clean dropdown menu instead of radio buttons
    selected_format_name = st.selectbox("Select Output Format:", list(FORMAT_OPTIONS.keys()))
    
    submitted = st.form_submit_button("⚙️ Convert Document", use_container_width=True)

# 4. PROCESS THE CONVERSION
if submitted:
    if not user_input.strip():
        st.warning("⚠️ Please paste some text before converting!")
    else:
        output_ext = FORMAT_OPTIONS[selected_format_name]
        output_file = f"Final_Document.{output_ext}"
        
        with st.spinner(f"Generating your {output_ext.upper()} file..."):
            try:
                # PDF requires the special LaTeX engine
                if output_ext == "pdf":
                    pypandoc.convert_text(user_input, 'pdf', format='md', outputfile=output_file, extra_args=['--pdf-engine=xelatex'])
                
                # HTML, Word, and EPUB look best with the "standalone" argument
                elif output_ext in ['docx', 'html', 'epub']:
                    pypandoc.convert_text(user_input, output_ext, format='md', outputfile=output_file, extra_args=['--standalone'])
                
                # All other formats (RTF, ODT, TEX)
                else:
                    pypandoc.convert_text(user_input, output_ext, format='md', outputfile=output_file)
                
                st.success(f"✅ Conversion successful! Click below to save your {output_ext.upper()} file.")
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label=f"⬇️ Download {selected_format_name}",
                        data=file,
                        file_name=output_file,
                        type="primary",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
