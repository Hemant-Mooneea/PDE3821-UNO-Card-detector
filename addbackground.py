from PIL import Image
import os
import random
import multiprocessing

# Paths to your UNO card images and background images
cards_folder = "images/uno_augmented"
backgrounds_folder = "images/backgroundrandom"
output_folder = "images/cards_with_backgrounds"

def overlay_card_on_background(card_image, background_image):
    """Overlay a card on a background at a random position."""
    # Resize the background
    background_image = background_image.resize((640, 640), Image.LANCZOS)

    # Get dimensions
    bg_width, bg_height = background_image.size

    # Maintain the aspect ratio of the card
    max_card_size = (200, 300)  # (max_width, max_height)
    card_aspect_ratio = card_image.width / card_image.height

    # Calculate new dimensions while maintaining the aspect ratio
    new_card_width = min(max_card_size[0], bg_width)
    new_card_height = int(new_card_width / card_aspect_ratio) if card_image.width > card_image.height else min(max_card_size[1], bg_height)
    new_card_width = int(new_card_height * card_aspect_ratio) if card_image.height > card_image.width else new_card_width

    # Resize the card
    card_image = card_image.resize((new_card_width, new_card_height), Image.LANCZOS)

    # Calculate random position for the card
    x = random.randint(0, bg_width - new_card_width)
    y = random.randint(0, bg_height - new_card_height)

    # Paste the card on the background
    background_image.paste(card_image, (x, y), card_image)

    return background_image

def process_card(card_filename, background_filenames):
    """Process a single card by overlaying it on a specific background."""
    card_path = os.path.join(cards_folder, card_filename)
    card_image = Image.open(card_path).convert("RGBA")

    # Determine the index of the background based on the card filename
    index = int(card_filename.split("img")[1][:3])  # Extract the index from the filename
    background_index = index % len(background_filenames)  # Wrap around if more cards than backgrounds

    # Choose the corresponding background
    background_filename = background_filenames[background_index]
    background_path = os.path.join(backgrounds_folder, background_filename)
    background_image = Image.open(background_path).convert("RGBA")

    # Overlay card on background and save the result
    combined_image = overlay_card_on_background(card_image, background_image)
    combined_image.save(os.path.join(output_folder, f"{card_filename}"), "PNG")

if __name__ == "__main__":
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load all card and background images
    card_filenames = [f for f in os.listdir(cards_folder) if f.endswith(('.png', '.jpg'))]
    background_filenames = [f for f in os.listdir(backgrounds_folder) if f.endswith(('.png', '.jpg'))]

    # Use multiprocessing to process cards in parallel
    with multiprocessing.Pool() as pool:
        pool.starmap(process_card, [(card_filename, background_filenames) for card_filename in card_filenames])

    print("Combination of cards and backgrounds completed!")
