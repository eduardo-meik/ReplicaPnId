import streamlit as st
from pdf_to_svg import convert_pdf_to_svg_and_tile
import tempfile
import os

st.title('PDF to SVG Converter with Tiling')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file to the temp directory
        pdf_path = os.path.join(temp_dir, 'uploaded.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(uploaded_file.read())
        
        # Convert PDF to SVG and create tiles
        convert_pdf_to_svg_and_tile(pdf_path, temp_dir)
        
        # Display download links for SVG files and tiles
        for filename in sorted(os.listdir(temp_dir)):
            if filename.endswith('.svg'):
                svg_file_path = os.path.join(temp_dir, filename)
                with open(svg_file_path, 'rb') as f:
                    st.download_button(
                        label=f"Download {filename}",
                        data=f,
                        file_name=filename,
                        mime='image/svg+xml'
                    )
