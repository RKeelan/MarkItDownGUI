# MarkItDown GUI

[![CI](https://github.com/RKeelan/MarkItDownGUI/actions/workflows/release.yml/badge.svg)](https://github.com/RKeelan/MarkItDownGUI/actions/workflows/release.yml)

A simple graphical user interface for Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) tool.

## Description

MarkItDown GUI provides an easy-to-use drag-and-drop interface for converting PDFs, Word documents, and PowerPoint slides to Markdown format. Simply drag files onto the application window and it will automatically convert them, generating markdown files in the same location as the original file.

## Usage

1. Run the application (`python main.py`) or by launching the executable.
2. Drag PDF (.pdf), Word (.docx), and PowerPoint (.pptx) files onto the application window
3. The application will convert them to Markdown and save the output files with the same name but .md extension

## Installation

1. Clone or download this repository
2. Install dependencies:

Using pip:
```
pip install -e .
```

Using UV:
```
pip install uv
uv venv .venv
uv pip install -e .
```

Or create a virtual environment with pip:
```
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Building as Standalone Executable

You can build a standalone executable using PyInstaller:

```
pyinstaller --onefile --windowed --icon icon.ico --add-data "icon.ico;." --collect-all magika --collect-all markitdown -n MarkItDownGUI.exe main.py
```

Or if you're using UV:

```
uv run pyinstaller --onefile --windowed --icon icon.ico --add-data "icon.ico;." --collect-all magika --collect-all markitdown -n MarkItDownGUI.exe main.py
```

The executable will be available in the `dist` directory.

## License

Use the same license as [MarkItDown](https://github.com/microsoft/markitdown).
