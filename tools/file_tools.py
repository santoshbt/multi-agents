from typing import List, Annotated, Optional, Dict
from langchain_core.tools import tool
import os

TEMP_DIR = os.path.join(os.getcwd(), "temp")

def _get_file_path(file_name: str) -> str:
    """ Construct the full file path and ensure the temp directory exists. """
    os.makedirs(TEMP_DIR, exist_ok=True)
    return os.path.join(TEMP_DIR, file_name)


@tool
def create_outline(
    points: Annotated[List[str], "List of main points or sections"],
    file_name: Annotated[str, "File path to save the outline"],
) -> Annotated[str, "Path of the saved outline file"]:
    """ Create and save an outline file
    """
    file_path = _get_file_path(file_name)
    # file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    # os.makedirs(os.path.dirname(file_to_use), exist_ok=True)
    with open(file_path, "w") as file:
        for i, point in enumerate(points):
            file.write(f"{i+1}. {point}\n")
    return f"Outline saved to {file_name}"

@tool
def read_document(
    file_name: Annotated[str, "File path to read the document from"],
    start: Annotated[Optional[int], "The start line, default is 0"] = None,
    end: Annotated[Optional[int], "The end line, default is None (read till end)"] = None,
):
    """ Read the specified document """
    file_path = _get_file_path(file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
    if start is None:
        start = 0
    return "\n".join(lines[start:end])



@tool
def write_document(
    content: Annotated[str, "Text content to be written to the document"],
    file_name: Annotated[str, "File path to save the document"]
):
    """ Create and save the text document """
    file_path = _get_file_path(file_name)
    with open(file_path, "w") as file:
        file.write(content)
    return f"Document saved to {file_name}"

@tool
def edit_document(
    file_name: Annotated[str, "File path to save the document"],
    insert: Annotated[Dict[int, str], "Dictionary with line number as key and text to insert as value"],
):
    """ Edit a document by inserting the text at specified line numbers """
    file_path = _get_file_path(file_name)
    with open(file_path, "w") as file:
        lines = file.readlines()

    sorted_inserts = sorted(inserts.items())

    for line_number, text in sorted_inserts:
        if 1 <= line_number <= len(lines) + 1:
            lines.insert(line_number-1, text + "\n")
        else:
            return f"Line number {line_number} is out of range."

    with open(file_path, "w") as file:
        file.writelines(lines)

    return f"Document {file_name} edited successfully."