from atlassian import Confluence
import os
from csharp_parser import extract_elements_with_references
from llm_summarizer import summarize_code
from config import CONFLUENCE_URL, CONFLUENCE_USER, CONFLUENCE_API_KEY, SPACE_KEY

confluence = Confluence(url=CONFLUENCE_URL, username=CONFLUENCE_USER, password=CONFLUENCE_API_KEY)

def create_script_page(file_path, parent_page_id, all_files):
    """ Create a Confluence page for a C# script, including function and field summaries with usage examples. """
    script_name = os.path.basename(file_path)
    
    elements = extract_elements_with_references(file_path, all_files)
    body = f"<h1>{script_name}</h1><p>Auto-generated documentation.</p>"

    for element in elements:
        summary = summarize_code(element['name'], element['type'], element['comment'], element['references'])
        body += f"<h2>{element['type'].capitalize()}: {element['name']}</h2>"
        body += f"<p><b>XML Comment:</b> {element['comment']}</p>"
        body += f"<p><b>LLM Summary:</b> {summary}</p>"

    confluence.create_page(
        space=SPACE_KEY,
        title=script_name,
        parent_id=parent_page_id,
        body=body,
        type="page"
    )