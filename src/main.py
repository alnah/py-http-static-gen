from textnode import TextNode, TextType


def main() -> None:
    text_node = TextNode(
        text="this is a text",
        text_type=TextType.BOLD,
        url="https://github.com/alnah/py-http-static-gen",
    )
    print(text_node)


if __name__ == "__main__":
    main()
