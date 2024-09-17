import PyPDF2

def loadPdfContent(file_path):
    """
    Load the content of a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The content of the PDF file.
    """
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader (file)
        content = ''
        for page in range(len(reader.pages)):
            content += reader.pages[page].extract_text()
    return content
