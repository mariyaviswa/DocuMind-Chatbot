import gradio as gr
from extractors.text_extract import extract_text
from embedding import embed_document, search_similar_chunks
from sentence_transformers import SentenceTransformer

# Load your embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global cache per file
faiss_index = None
chunks = []

def process_file(file):
    global faiss_index, chunks
    if file is None:
        return "No file uploaded.", "", ""

    file_path = file.name
    try:
        result = extract_text(file_path)
        text = result["texts"]
        metadata = result["meta_data"]

        # Embedding
        faiss_index, chunks, _ = embed_document(text)

        meta_str = (
            f"**File Name:** {metadata['fileName']}\n"
            f"**File Type:** {metadata['fileType']}\n"
            f"**Total Pages/Rows:** {metadata['numberOfPages']}"
        )

        return meta_str, text, ""

    except Exception as e:
        return f"❌ Error: {str(e)}", "", ""

def answer_question(query):
    if not faiss_index or not chunks:
        return "Please upload a document first."
    top_chunks = search_similar_chunks(query, model, faiss_index, chunks)
    combined_context = "\n\n".join(top_chunks)
    return f"📚 Top Relevant Text:\n\n{combined_context}"
    # (Optional) Add LLM answer here

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 📄 Document Intelligence with Search")
    gr.Markdown("Upload a document, extract text & metadata, and ask questions about its content.")

    with gr.Row():
        file_input = gr.File(label="📂 Upload Document", file_types=[".pdf", ".docx", ".csv", ".xls", ".xlsx"])

    with gr.Row():
        metadata_output = gr.Markdown(label="📑 Metadata")
        text_output = gr.Textbox(label="📝 Extracted Text", lines=20, show_copy_button=True)

    with gr.Row():
        question_input = gr.Textbox(label="❓ Ask a Question", placeholder="E.g., What is the document about?")
        answer_output = gr.Textbox(label="🤖 Retrieved Answer", lines=8)

    file_input.change(fn=process_file, inputs=file_input, outputs=[metadata_output, text_output, answer_output])
    question_input.submit(fn=answer_question, inputs=question_input, outputs=answer_output)

if __name__ == "__main__":
    demo.launch()
