from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import random
import os
import numpy as np
import time
import multiprocessing as mp

input_folder = "images/uno_normal"
output_folder = "images/uno_augmented"

# Number of rounds to augment each card
num_rounds = 185
def random_color_adjustments(card):
    """Applies random color adjustments like brightness, contrast, and saturation."""
    brightness = ImageEnhance.Brightness(card)
    card = brightness.enhance(random.uniform(0.6, 1.5))  

    contrast = ImageEnhance.Contrast(card)
    card = contrast.enhance(random.uniform(0.8, 1.5)) 

    color = ImageEnhance.Color(card)
    card = color.enhance(random.uniform(0.8, 1.5))  

    return card

def random_rotation(card):
    """Applies a small random rotation to simulate different viewing angles."""
    angle = random.randint(-90, 90)
    return card.rotate(angle, expand=True)

def random_scaling(card):
    """Randomly scales the card."""
    scale_factor = random.uniform(1.0, 2.0)  
    new_size = (int(card.width * scale_factor), int(card.height * scale_factor))
    return card.resize(new_size)

def add_noise(card):
    """Adds subtle Gaussian noise to the visible parts of the card."""
    card_np = np.array(card)

    # Create a mask where alpha is greater than 0 (non-transparent areas)
    mask = card_np[..., 3] > 0
    noise_std_dev = 0.65
    noise = np.random.normal(0, noise_std_dev, card_np.shape).astype(np.uint8)

    # Apply noise only to the non-transparent areas
    card_np[mask] = np.clip(card_np[mask] + noise[mask], 0, 255)
    
    return Image.fromarray(card_np)

def random_shadow(card):
    """Adds a semi-transparent shadow only to the visible parts of the card."""
    # Create a shadow image with a random alpha value
    shadow_alpha = random.randint(50, 100)
    shadow = Image.new('RGBA', card.size, (0, 0, 0, shadow_alpha))

    # Convert card image and shadow to NumPy arrays
    card_np = np.array(card)
    shadow_np = np.array(shadow)

    # Create a mask for the visible parts of the card (where alpha > 0)
    mask = card_np[..., 3] > 0

    # Blend the card and shadow only where the mask is True
    combined_np = card_np.copy()  # Start with the original card

    # Apply the shadow where the card is visible
    combined_np[mask, :3] = np.clip(card_np[mask, :3] + shadow_np[mask, :3] * (shadow_alpha / 255.0), 0, 255)

    return Image.fromarray(combined_np, 'RGBA')

def add_dust_spots(card):
    """Adds small dust spots for a worn or imperfect look."""
    draw = ImageDraw.Draw(card)
    for _ in range(random.randint(5, 15)):
        x, y = random.randint(0, card.width), random.randint(0, card.height)
        draw.ellipse([x, y, x + 2, y + 2], fill=(random.randint(50, 100),) * 3)
    return card

def add_blur(card):
    """Applies a subtle Gaussian blur to the card image."""
    if random.choice([True, False]):
        blur_radius = random.uniform(0.1, 10)
        return card.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return card

def color_tint(card):
    r, g, b = random.uniform(0.9, 1.1), random.uniform(0.9, 1.1), random.uniform(0.9, 1.1)
    card_np = np.array(card)
    card_np[..., 0] = np.clip(card_np[..., 0] * r, 0, 255)
    card_np[..., 1] = np.clip(card_np[..., 1] * g, 0, 255)
    card_np[..., 2] = np.clip(card_np[..., 2] * b, 0, 255)
    return Image.fromarray(card_np)

def apply_occlusion(card):
    """
    Applies rectangular occlusions on visible (non-transparent) areas of the card.
    Occlusions are intended to simulate real-world obstructions for model training.
    """
    # Convert card to NumPy array to process transparency
    card_np = np.array(card)
    visible_mask = card_np[..., 3] > 0  # Non-transparent areas

    # Find boundaries of the visible area
    y_coords, x_coords = np.where(visible_mask)
    if len(y_coords) == 0 or len(x_coords) == 0:
        print("No visible area found; returning original card.")
        return card

    # Calculate bounds and occlusion dimensions
    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)
    width, height = max_x - min_x, max_y - min_y
    rect_width, rect_height = max(int(0.2 * width), 1), max(int(0.2 * height), 1)

    # Create a copy of the image to apply occlusions
    card_copy = card.copy()
    draw = ImageDraw.Draw(card_copy)

    # Apply 1-2 occlusions
    for _ in range(random.randint(1, 2)):
        for attempt in range(10):  # Max 10 attempts to place occlusion
            # Randomly place within safe bounds
            safe_x = random.randint(min_x, max_x - rect_width)
            safe_y = random.randint(min_y, max_y - rect_height)

            # Check if rectangle fits entirely in visible area
            if visible_mask[safe_y:safe_y + rect_height, safe_x:safe_x + rect_width].all():
                draw.rectangle(
                    [safe_x, safe_y, safe_x + rect_width, safe_y + rect_height],
                    fill=(255, random.randint(0, 255), random.randint(0, 255), random.randint(50, 200))
                )
                break

    return card_copy

def augment_and_save_card(filename):
    """Augments a single card image and saves it."""
    num_occluded_rounds = int(num_rounds * 0.15)  # 15% of the rounds will have occlusions
    occluded_rounds = random.sample(range(num_rounds), num_occluded_rounds)  # Randomly select rounds to have occlusions
    
    for round in range(num_rounds):
        card = Image.open(os.path.join(input_folder, filename)).convert("RGBA")

        # Apply augmentations in an optimized order
        card = random_scaling(card)
        
        # Check if the current round is one of the occluded rounds
        if round in occluded_rounds:
            card = apply_occlusion(card)
        
        card = random_color_adjustments(card)
        card = random_rotation(card)
        card = add_noise(card)
        card = random_shadow(card)
        card = add_dust_spots(card)
        card = add_blur(card)
        card = color_tint(card)
        
        # Save the augmented image
        name, ext = os.path.splitext(filename)
        output_filename = os.path.join(output_folder, f"{name}_img{round:03d}.png")
        card.save(output_filename, "PNG")

if __name__ == "__main__":
    os.makedirs(output_folder, exist_ok=True)
    
    start_time = time.time()
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(augment_and_save_card, [filename for filename in os.listdir(input_folder) if filename.endswith(".png")])
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    print("Augmentation completed!")
