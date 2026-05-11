import re
from langchain_core.documents import Document

def parse_qa_markdown(text: str) -> list[Document]:
    """
    Parses a Markdown text containing Q&A pairs separated by empty lines.
    Format expected:
    问：[Question]
    答：[Answer]
    """
    documents = []
    # Split text into blocks separated by one or more empty lines
    blocks = re.split(r'\n\s*\n', text.strip())

    for idx, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue

        # We can just store the whole block as the page_content to keep Q&A intact.
        # This gives the LLM both the question and answer for context.
        # Alternatively, we can use metadata. Let's just store the block.
        if "问：" in block and "答：" in block:
            doc = Document(
                page_content=block,
                metadata={"source": "QA_Document", "block_index": idx}
            )
            documents.append(doc)

    return documents

def read_and_parse_file(filepath: str) -> list[Document]:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return parse_qa_markdown(text)
