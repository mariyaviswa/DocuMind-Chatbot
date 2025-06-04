from docx import Document

def extract_text_from_word(file_path):
    doc = Document(file_path)
    return doc
    # # Extract all the texts from each paragraphs
    # contents = '\n'.join([para.text for para in doc.paragraphs])

    # return contents

print(extract_text_from_word("D:/Downloads/IMCV QP.docx"))