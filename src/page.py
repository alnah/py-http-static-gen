from logger import get_logger
from converter import markdown_text_to_html_node
import os


class MarkdownTitleError(Exception):
    pass


def extract_title(text: str) -> str:
    if not text:
        raise ValueError("Markdown document can't be empty")

    if not text.startswith("# "):
        raise MarkdownTitleError('Markdown document must start with "# Your Title"')

    for i in range(2, 7):
        if text.startswith(f"{'#' * i} "):
            raise MarkdownTitleError(
                f"Expected heading level 1, got level {i}: {'#' * i}"
            )

    return text.lstrip("# ").strip()


def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filepath {file_path} doesn't exist")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def write_file(file_path: str, data: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
    except IOError as e:
        raise IOError(f'Could not write data to "{file_path}": {e}')


def generate_page(template_path: str, src_path: str, dst_path: str) -> None:
    logger = get_logger()
    template, markdown = read_file(template_path), read_file(src_path)
    html = markdown_text_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    logger.info(html)
    write_file(dst_path, page)
    logger.info(f'Generated page: from "{src_path}" to "{dst_path}"')
