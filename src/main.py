from copytree import copytree
from page import generate_pages_recursive


def main() -> None:
    """Copy static files and generate pages for the site."""
    copytree("static", "public")
    generate_pages_recursive("template.html", "content/", "public/")


if __name__ == "__main__":
    main()
