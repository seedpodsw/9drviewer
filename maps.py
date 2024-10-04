import os
from PIL import Image
from tqdm import tqdm
import re

folder_path = './images'
output_file = './maps.js'
js_objects = []
png_files = [file_name for file_name in os.listdir(folder_path) if file_name.endswith('.png')]

# Set up the progress bar
with tqdm(total=len(png_files), desc="Processing images", leave=True) as pbar:
    for file_name in png_files:
        file_path = os.path.join(folder_path, file_name)

        try:
            with Image.open(file_path) as img:
                width, height = img.size

            # Create a human-readable label by stripping unnecessary characters
            label = re.sub(r'[_\-]', ' ', file_name)  # Replace underscores and hyphens with spaces
            label = re.sub(r'^\d+\s*|\.\w+$', '', label)  # Remove leading numbers and file extension
            label = label.strip().title()  # Trim leading/trailing spaces and title-case it

            js_objects.append(f"{{ filename: '{file_name}', width: {width}, height: {height}, label: '{label}' }}")

        except Exception as e:
            tqdm.write(f"Failed to process {file_name}: {e}")

        pbar.update(1)

js_output = 'export const imageMaps = [\n' + ',\n'.join(js_objects) + '\n];'

with open(output_file, 'w') as f:
    f.write(js_output)

tqdm.write(f"JavaScript object format with dimensions written to {output_file}")
