import os
import random
import shutil

def randomize_image_names(source_folder, target_folder):
    # Create target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # List all files in the source folder
    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # Shuffle the image files for random order
    random.shuffle(image_files)

    # Process each image file
    for index, filename in enumerate(image_files):
        # Generate a new random name for each image
        new_filename = f"image_{index:04d}{os.path.splitext(filename)[1]}"
        
        # Define the source and target file paths
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, new_filename)

        # Copy the image with the new name
        shutil.copy2(source_path, target_path)
        print(f"Copied and renamed {filename} to {new_filename}")

    print("Image renaming and copying completed.")

# Example usage
source_folder = "images/backgrounds"
target_folder = "images/backgroundrandom"
randomize_image_names(source_folder, target_folder)
