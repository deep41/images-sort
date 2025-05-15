#!/usr/bin/env python3

import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageRenamePrep:
    def __init__(self, input_folder="images", output_csv="rename_map.csv"):
        """Initialize the Image Rename Preparation script.
        
        Args:
            input_folder (str): Path to the folder containing images
            output_csv (str): Path where the CSV mapping will be saved
        """
        self.input_folder = Path(input_folder)
        self.output_csv = Path(output_csv)
        self.image_extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
        
    def get_image_datetime(self, image_path):
        """Extract the creation datetime from image EXIF data.
        
        Args:
            image_path (Path): Path to the image file
            
        Returns:
            tuple: (datetime object, success boolean)
        """
        try:
            with Image.open(image_path) as img:
                exif = img._getexif()
                if not exif:
                    logger.warning(f"No EXIF data found for {image_path}")
                    return None, False
                
                # Try to get DateTimeOriginal (tag 36867)
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        date_str = exif[tag_id]
                        try:
                            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S'), True
                        except ValueError:
                            logger.error(f"Invalid datetime format in {image_path}")
                            return None, False
                
                # Fallback to file modification time
                logger.warning(f"No DateTimeOriginal found for {image_path}, using file mtime")
                return datetime.fromtimestamp(os.path.getmtime(image_path)), True
                
        except Exception as e:
            logger.error(f"Error processing {image_path}: {str(e)}")
            return None, False
    
    def process_images(self):
        """Process all images in the input folder and generate rename mapping."""
        # Get all image files
        image_files = []
        for ext in self.image_extensions:
            image_files.extend(list(self.input_folder.glob(f"*{ext}")))
        
        if not image_files:
            logger.error(f"No image files found in {self.input_folder}")
            return False
        
        # Process each image and collect metadata
        image_data = []
        for img_path in tqdm(image_files, desc="Processing images"):
            datetime_obj, success = self.get_image_datetime(img_path)
            if success:
                image_data.append({
                    'original_path': img_path,
                    'datetime': datetime_obj,
                    'filename': img_path.name
                })
            else:
                logger.warning(f"Skipping {img_path} due to metadata extraction failure")
        
        if not image_data:
            logger.error("No valid images found to process")
            return False
        
        # Sort images by datetime and filename (for tie-breaking)
        image_data.sort(key=lambda x: (x['datetime'], x['filename']))
        
        # Generate new filenames
        rename_mapping = []
        for idx, img_data in enumerate(image_data, start=1):
            new_filename = f"IMG_{idx:04d}.jpg"
            rename_mapping.append({
                'OriginalFilename': img_data['filename'],
                'NewFilename': new_filename
            })
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(rename_mapping)
        df.to_csv(self.output_csv, index=False)
        logger.info(f"Successfully created rename mapping at {self.output_csv}")
        logger.info(f"Processed {len(rename_mapping)} images")
        return True

def main():
    """Main entry point for the script."""
    renamer = ImageRenamePrep()
    renamer.process_images()

if __name__ == "__main__":
    main() 