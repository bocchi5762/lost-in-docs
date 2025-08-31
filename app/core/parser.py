import pymupdf
import pymupdf4llm

from langchain_text_splitters import MarkdownHeaderTextSplitter


def parse_pdf(pdf_content: bytes):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    
    pdf_document = pymupdf.open(stream=pdf_content, filetype="pdf")
    md_text = pymupdf4llm.to_markdown(doc=pdf_document)

    md_header_splits = markdown_splitter.split_text(md_text)

    return md_header_splits