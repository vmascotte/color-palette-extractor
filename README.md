# Color Palette Extractor

This small script extracts a color palette from an image using K-means clustering.

## Requirements

Install dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python palette.py path/to/image.jpg [n_cores]
```

- `path/to/image.jpg` – Path to the image file
- `n_cores` – Optional number of colors to extract. Defaults to 5 if omitted.

The script will print one hexadecimal color per line representing the extracted palette.
