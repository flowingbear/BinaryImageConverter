
# Binary-Image Converter

A tool to convert any binary file into an image (PNG) and back. This can be useful for visually representing binary data or sharing binary files through image-sharing platforms.

## Features

- Convert any binary file to a PNG image
- Restore binary files from converted images
- Progress indicator for large files
- Support for files with non-ASCII filenames

## Requirements

- Python 3.6 or higher
- NumPy
- Pillow (PIL)

## Installation

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/windows/)
2. Open Command Prompt and run:
```
pip install numpy pillow
```
3. Download or clone this repository

### macOS

1. Install Python (if not already installed):
```
brew install python
```
2. Install the required packages:
```
pip3 install numpy pillow
```
3. Download or clone this repository

## Usage

### Converting a Binary File to an Image

```
python binary2jpg.py input_file output_image.png --mode bin2jpg
```

### Converting an Image Back to Binary

```
python binary2jpg.py input_image.png output_file --mode jpg2bin
```

### Examples

Convert an MP3 file to an image:
```
python binary2jpg.py song.mp3 song_image.png --mode bin2jpg
```

Restore the MP3 from the image:
```
python binary2jpg.py song_image.png restored_song.mp3 --mode jpg2bin
```

## Important Notes

- Always use PNG as the output format when converting binary to image to ensure lossless conversion
- Only use images created with this tool when converting back to binary
- The conversion preserves the original filename (up to 16 characters)

## Project Structure

- `binary2jpg.py`: Main script with command-line interface
- `converter.py`: Core conversion logic
- `utils.py`: Helper functions for file validation and progress display

## License

This project is open source and available under the MIT License.
