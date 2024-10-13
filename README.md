# Image Compression and Conversion Tool

This project provides a simple Python tool to load JPEG/PNG images from a folder, compress them, and convert them to a
multi-page TIFF file. It uses object-oriented principles, dependency injection, and supports configurable DPI and color
spaces.

## Features

- Load JPEG/PNG images from a directory.
- Convert images to TIFF format with customizable compression.
- Supports different color spaces (e.g., `RGB`, `YCbCr`).
- Configurable DPI settings (default: `100x100`).
- Error handling for corrupted or unreadable image files.

## Requirements

- Python 3.x
- [Pillow](https://python-pillow.org/) library for image processing

You can install the required Python packages by running:

```bash
pip install Pillow
```

## Usage

### Main Functionality

The tool processes a folder of images and converts them into a multi-page TIFF file. The conversion settings (
compression type, quality, color space) can be adjusted as per the use case.

### Steps to Run:

1. Place all your images (`.jpg`, `.jpeg`, `.png`) in a folder (default: `"Images"`).
2. Run the Python script `main.py` using the command:

```bash
python main.py
```

The output file will be saved as `output_compressed.tif`.

### Default Settings

- **Input Folder**: `"Images"`
- **Output File**: `"output_compressed.tif"`
- **Compression**: `"jpeg"` (lossy JPEG compression within TIFF)
- **Color Space**: `"YCbCr"` (you can change this to `"RGB"` if needed)
- **Quality**: `30` (compression quality, lower values result in higher compression)
- **DPI**: Derived from the image metadata or default `100x100`.

### Code Structure

- **ImageCompressor**: Abstract base class for handling image compression.
- **JpegToTiffConverter**: Handles the conversion of JPEG/PNG images to multi-page TIFF with DPI and compression
  settings.
- **ImageLoader**: Abstract base class for loading images.
- **JpegImageLoader**: Loads images from a folder and converts them to a specified color space, extracting DPI if
  available.
- **ImageProcessor**: The main processor class that orchestrates image loading and conversion via dependency injection.

### Example Configuration

To customize the behavior of the script, you can modify the following variables inside the `main()` function in
`main.py`:

```python
folder_path = "testImages"  # Path to the folder containing input images
output_file = "output_compressed.tif"  # Path to save the converted TIFF file
compression = "jpeg"  # Compression type: "jpeg", "tiff_adobe_deflate", etc.
color_space = "YCbCr"  # Color space: "RGB" or "YCbCr"
quality = 30  # Compression quality (lower values = higher compression)
```

### Example Configuration

```bash
python main.py
```

On successful execution, the console will output:

```bash
Conversion completed. Output saved as output_compressed.tif.
```

### Error Handling

If any image cannot be loaded (e.g., due to corruption), an error message will be displayed for that image, and the
program will continue processing other images.

### Customization

You can extend or modify the following components:

- Compression: Extend ImageCompressor to support other image formats or compression techniques.
- Color Space: Modify the color_space parameter to use different image color modes such as "RGB" or "YCbCr".
- DPI: The DPI can be customized or extracted from the image metadata. If no DPI is found, a default value of 100x100 is
  used.

### Future Enhancements

Some possible future improvements to the tool include:

- Adding support for more image formats.
- Allowing batch processing with multithreading for faster conversion.
- Adding command-line arguments for easier configuration without modifying the script.

### License

This project is open-source and free to use.
