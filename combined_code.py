import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import docx2txt
import pdfplumber
import time
import PyPDF2
import fitz
import io
import cv2
import pytesseract
from PIL import Image
import abstract_summarization as ast
import output

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'

def extract_content_image(file):
    content = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf_file:
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            page_content = page.get_text()
            if page_content:
                content = content + "\n" +page_content + "\n"
            image_list = page.getImageList()
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.getImageList(), start=1):
                xref = img[0]
                print("")
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]

                image_ext = base_image["ext"]
                #image = Image.open(io.BytesIO(image_bytes))
                #image.save(open(f"image{page_index + 1}_{image_index}.{image_ext}", "wb"))
                print(f"image{page_index + 1}_{image_index}.{image_ext}")
                image = Image.open(f"image{page_index + 1}_{image_index}.{image_ext}")
                text = pytesseract.image_to_string(image)
                if text:
                    content = content + "\n" + text + "\n"

        return content

def load_image(image_file):
    img = Image.open(image_file)
    return img

def main():
    st.title("                  Text Summarisation                 ")
    st.header("Input File Upload ")

    menu = ["Text files", "Word documents", "PDF files", "Image files"]
    choice = st.selectbox("Select file type", menu)

    if choice == "Text files":
        docx_file = st.file_uploader("Upload File", type=['txt'])
        if st.button("Process"):
            if docx_file is not None:
                file_details = {"Filename": docx_file.name, "FileType": docx_file.type, "FileSize": docx_file.size}
                if docx_file.type == "text/plain":
                    raw_text = str(docx_file.read(),
                                   "utf-8")
                    summary = ast.summarize(raw_text)
                    output.format_output(docx_file.name, summary)

    elif choice == "PDF files":
        docx_file = st.file_uploader("Upload File", type=['pdf'])
        if st.button("Process"):
            if docx_file is not None:
                if docx_file.type == "application/pdf":
                    try:
                        img_and_text = extract_content_image(docx_file)
                        summary = ast.summarize(img_and_text)
                        #print(summary)
                        output.format_output(docx_file.name, summary)
                    except:
                        st.write("None")

    elif choice == "Word documents":
        docx_file = st.file_uploader("Upload File", type=['docx'])
        if st.button("Process"):
            if docx_file is not None:
                if docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    raw_text = docx2txt.process(docx_file)
                    summary = ast.summarize(raw_text)
                    output.format_output(docx_file.name, summary)

    elif choice == "Image files":
        image_file = st.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
        if st.button("Process"):
            if image_file is not None:
                img = load_image(image_file)
                image = Image.open(image_file)
                text = pytesseract.image_to_string(image)
                summary = ast.summarize(text)
                output.format_output(image_file.name, summary)

if __name__ == '__main__':
    main()
