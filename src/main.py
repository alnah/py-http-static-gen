from copytree import copytree


def main() -> None:
    copytree("static", "public")


if __name__ == "__main__":
    main()
