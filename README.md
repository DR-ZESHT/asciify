# asccify

**asciify** is a lightweight, open-source Python tool to convert images into ASCII art. This project uses the `Pillow` library to transform any color image into a combination of text characters.

## Features

* Supports multiple image formats (PNG, JPG, JPEG, BMP, etc.)
* Color or grayscale output
* Adjustable output width
* Save output to a text file
* Direct display in terminal

## Installation

Make sure Python is installed on your system, then install the `Pillow` library:

```bash
pip install pillow
```

## Usage

### Simple execution and display in terminal

```bash
python deamonart.py input.jpg
```

### Save output to a file

```bash
python deamonart.py input.jpg --out art.txt
```

### Optional parameters

* `--width`, `-w`: Set output width (default: 80)
* `--invert`: Invert brightness mapping
* `--color`: ANSI colored output
* `--ramp`: Define character ramp from dark to light
* `--contrast`: Adjust image contrast (default: 1.0)
* `--brightness`: Adjust image brightness (default: 1.0)

## Example

```bash
python deamonart.py photo.jpg -w 100 --color --out ascii.txt
```

## License

This project is licensed under the MIT License.
