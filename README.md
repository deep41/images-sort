# Image Renaming Preparation Script

This script prepares a mapping for renaming image files based on their chronological order, determined by EXIF metadata timestamps. It generates a CSV file containing the mapping between current filenames and proposed new filenames without actually performing the renaming.

## Features

- Reads image files from a designated input folder
- Extracts timestamp information from image metadata (EXIF DateTimeOriginal)
- Sorts images chronologically with filename-based tie-breaking
- Generates sequential filenames in the format IMG_XXXX.jpg
- Produces a CSV report with original and proposed new filenames
- Handles common errors gracefully

## Requirements

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - Pillow (for image processing and EXIF data)
  - pandas (for CSV handling)
  - tqdm (for progress bars)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your images in the `images/` directory
2. Run the script:
   ```bash
   python image_rename_prep.py
   ```
3. Check the generated `rename_map.csv` file for the proposed filename mappings

## Output

The script generates a CSV file (`rename_map.csv`) with two columns:
- `OriginalFilename`: The current filename of the image
- `NewFilename`: The proposed new filename (format: IMG_XXXX.jpg)

## Error Handling

The script handles several error cases:
- Missing EXIF data: Falls back to file modification time
- Unreadable images: Skips the file and logs a warning
- Invalid datetime formats: Skips the file and logs an error
- No images found: Logs an error and exits

## Notes

- Only processes files in the top-level of the images/ directory (no subdirectories)
- Supports common image formats (.jpg, .jpeg, .JPG, .JPEG)
- Does not perform actual file renaming
- New filenames will always use lowercase .jpg extension 