#!/usr/bin/env python3

import csv
import os
from pathlib import Path

def generate_rename_script():
    # Read the CSV file
    with open('rename_map.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Create a shell script with mv commands
        with open('rename_images.sh', 'w') as shellfile:
            # Add shebang and safety flags
            shellfile.write('#!/bin/bash\n\n')
            shellfile.write('# Exit on error\nset -e\n\n')
            shellfile.write('# Change to the images directory\ncd images\n\n')
            
            # Add a header comment
            shellfile.write('# Generated mv commands for renaming images\n\n')
            
            # Generate mv commands for each row
            for row in reader:
                original = row['OriginalFilename']
                new = row['NewFilename']
                
                # Escape spaces and special characters in filenames
                original_escaped = original.replace(' ', '\\ ')
                new_escaped = new.replace(' ', '\\ ')
                
                # Write the mv command
                shellfile.write(f'mv "{original}" "{new}"\n')
            
            shellfile.write('\necho "All files have been renamed successfully!"\n')

    # Make the shell script executable
    os.chmod('rename_images.sh', 0o755)
    print("Generated rename_images.sh - Review the script and run it to rename the files.")

if __name__ == "__main__":
    generate_rename_script() 