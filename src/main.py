from converter import markdown_text_to_html_node


def main() -> None:
    text = '# This is a heading, and **bold**, and *italic*, and _italic_, and \
`code`, and ![image](https://image.com), and [link](https://link.com)\n\n\
## This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
#### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
##### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
###### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
This is a paragraph, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
```python\nprint("Hello, World!")\n```\n\n\
> This is a quote, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
* This is a normal text\n\
* This is a **bold** text\n\
* This is an *italic* text\n\
* This is an _italic_ text\n\
* This is a `code` text\n\
* This is an ![image](https://image.com)\n\
* This is a [link](https://link.com)\n\n\
- This is a normal text\n\
- This is a **bold** text\n\
- This is an *italic* text\n\
- This is an _italic_ text\n\
- This is a `code` text\n\
- This is an ![image](https://image.com)\n\
- This is a [link](https://link.com)\n\n\
1. This is a normal text\n\
2. This is a **bold** text\n\
3. This is an *italic* text\n\
4. This is an _italic_ text\n\
5. This is a `code` text\n\
6. This is an ![image](https://image.com)\n\
7. This is a [link](https://link.com)'
    html_node = markdown_text_to_html_node(text)
    print(html_node.to_html())


if __name__ == "__main__":
    main()
