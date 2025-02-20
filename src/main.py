from converter import markdown_text_to_blocks


def main() -> None:
    text = "   whitespaces   \n\n    another whitespaces   \n\n\n hello \n\n\n\n world \n\n"
    blocks = markdown_text_to_blocks(text)
    print(blocks)


if __name__ == "__main__":
    main()
