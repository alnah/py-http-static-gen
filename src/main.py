from nodeconv import text_to_text_nodes


def main() -> None:
    text = "This is a text with **bold**, and *italic*, and _italic_, and `code`\
, and ![image](https://image.com) and [link](https://link.com)"
    nodes = text_to_text_nodes(text)
    for node in nodes:
        print(node)


if __name__ == "__main__":
    main()
