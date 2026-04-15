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
st.title("📄 Waleed's MS Word & PDF Converter")
st.markdown("""
Welcome! Paste your AI-generated text (including math equations surrounded by `$$`) into the box below. 
Select your output format, and instantly download a perfectly formatted document.
""")

with st.form("converter_form"):
    user_input = st.text_area(
        "Paste your text here (Ensure a space after hashtags, e.g., '# Heading'):", 
        height=300
    )
    
    # NEW: Dropdown to choose between Word and PDF
    format_choice = st.radio("Select Output Format:", ["MS Word (.docx)", "PDF (.pdf)"], horizontal=True)
    
    submitted = st.form_submit_button("⚙️ Convert Document", use_container_width=True)

# 4. PROCESS THE CONVERSION
if submitted:
    if not user_input.strip():
        st.warning("⚠️ Please paste some text before converting!")
    else:
        # PDFs take a bit longer to process, so we warn the user
        with st.spinner(f"Generating your {format_choice} file... (PDFs may take 10-15 seconds)"):
            try:
                if format_choice == "MS Word (.docx)":
                    output_file = "Final_Document.docx"
                    # The '--standalone' argument fixes the heading sizes in MS Word!
                    pypandoc.convert_text(user_input, 'docx', format='md', outputfile=output_file, extra_args=['--standalone'])
                    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                
                else:
                    output_file = "Final_Document.pdf"
                    # We use xelatex engine specifically because it handles complex math beautifully
                    pypandoc.convert_text(user_input, 'pdf', format='md', outputfile=output_file, extra_args=['--pdf-engine=xelatex'])
                    mime_type = "application/pdf"
                
                st.success("✅ Conversion successful! Click below to save your file.")
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label=f"⬇️ Download {format_choice}",
                        data=file,
                        file_name=output_file,
                        mime=mime_type,
                        type="primary",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
