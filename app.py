import gradio as gr
import os
from extractors.text_extract import extract_text

def process_file(file: str):
    if file is None:
        return "No file uploaded.", ""

    file_path = file.name
    try:
        result = extract_text(file_path)
        metadata = result["meta_data"]
        text = result["texts"]

        # Format metadata nicely
        meta_str = (
            f"**File Name:** {metadata['fileName']}\n"
            f"**File Type:** {metadata['fileType']}\n"
            f"**Total Pages/Rows:** {metadata['numberOfPages']}"
        )

        return meta_str, text

    except Exception as e:
        return f"Error: {str(e)}", ""

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 📄 Document Text & Metadata Extractor")
    gr.Markdown("Upload a PDF, Word, CSV, or Excel file to extract its text and key metadata.")

    with gr.Row():
        file_input = gr.File(label="Upload Your Document", file_types=[".pdf", ".docx", ".csv", ".xls", ".xlsx"])

    with gr.Row():
        metadata_output = gr.Markdown(label="📑 Metadata")
        text_output = gr.Textbox(label="📝 Extracted Text", lines=25, show_copy_button=True)

    file_input.change(fn=process_file, inputs=file_input, outputs=[metadata_output, text_output])

# Launch
if __name__ == "__main__":
    demo.launch(share=True)
