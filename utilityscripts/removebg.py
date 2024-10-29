from rembg import remove
from PIL import Image
import os

input_folder = "images/uno"
output_folder = "images/unorotated"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")  # Save as PNG

        # Open the input image
        input_image = Image.open(input_path)

        # Remove the background
        output_image = remove(input_image)

        # Rotate the image 90 degrees to the right
        output_image = output_image.rotate(-90, expand=True)

        # Save the processed image as PNG
        output_image.save(output_path)

print("Background removal and processing completed!")
