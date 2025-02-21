import os

from converter import markdown_text_to_html_node
from logger import get_logger


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
    try:
        template, markdown = read_file(template_path), read_file(src_path)
        html = markdown_text_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
        if src_path.endswith(".md"):
            dst_path = dst_path.rsplit(".", 1)[0] + ".html"
            write_file(dst_path, page)
    except Exception as e:
        logger.info(e)
    logger.info(f'Generated page: from "{src_path}" to "{dst_path}"')


def generate_pages_recursive(
    template_path: str,
    current_src: str,
    current_dst: str,
) -> None:
    logger = get_logger()
    os.makedirs(current_dst, exist_ok=True)
    for branch in os.listdir(current_src):
        src_path = os.path.join(current_src, branch)
        dst_path = os.path.join(current_dst, branch)
        if os.path.isfile(src_path):
            generate_page(template_path, src_path, dst_path)
        elif os.path.isdir(src_path):
            generate_pages_recursive(template_path, src_path, dst_path)
    logger.info(f'Generated all pages: from "{current_src}" to {current_dst}"')
