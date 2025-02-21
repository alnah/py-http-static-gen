# py-static-site-gen

A static site generator built from scratch using only the Python Standard Library at runtime.
It converts Markdown into HTML.
This project explores the fundamental mechanics behind popular tools like Jekyll, Hugo, and Gatsby.

## Installation

Before proceeding, ensure that Python is installed on your system. Then:

```
git clone https://github.com/alnah/py-static-site-gen && cd py-static-site-gen
make
```

## Usage

The app includes some default Markdown files in the `content/` folder.
Feel free to delete them and organize your own files.
Let's add a new `index.md` file at the root of our `content/` directory:

```
echo '# My First Page' > content/index.md
```

You can add static files in the `static/` folder.
The `make` command will recursively copies its content into the `public/` directory and serves it.
For example, add a new image:

```
curl -o static/images/my_first_image.jpg https://i.imgur.com/ZPZgYLC.jpeg
```

Update your `content/index.md` file to reference the downloaded image.

```
echo '\n![My First Image](/images/my_first_image.jpg)' >> content/index.md
```

Run the HTTP server again:

```
make
```

You can also run the unit tests:

```
make test
```

## Development Dependencies

The application only requires the Python Standard Library at runtime.
However, I used some development tools:

For the codebase:

- [pyright](https://github.com/microsoft/pyright) for static type checking.
- [ruff](https://github.com/astral-sh/ruff) for formatting and linting.

For my Helix editor configuration:

- [python-lsp-server](https://github.com/python-lsp/python-lsp-server) for code completion and syntax highlighting.
- [pylsp-rope](https://github.com/python-rope/pylsp-rope) for refactoring.

## License

This project is distributed under the Apache License. See the [LICENSE](LICENSE) file for more details.
