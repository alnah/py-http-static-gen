from copytree import copytree
from page import generate_page


def main() -> None:
    copytree("static", "public")
    generate_page("template.html", "content/index.md", "public/index.html")


if __name__ == "__main__":
    main()
