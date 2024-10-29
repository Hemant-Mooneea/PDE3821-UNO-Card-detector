import os
import shutil
from collections import defaultdict
import random
from pathlib import Path
import re

def extract_image_info(filename):
    # Extract card type and image number from filename
    # Example: "+4_img000" -> ("+4", "000")
    match = re.match(r'(.+)_img(\d+)', filename)
    if match:
        card_type, img_num = match.groups()
        return card_type, img_num
    return None, None

def split_dataset(source_dir, train_dir, val_dir, test_dir, train_ratio=0.7, val_ratio=0.1):
    # Create directories if they don't exist
    for directory in [train_dir, val_dir, test_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # First, group files by background number
    background_groups = defaultdict(list)
    
    # Get all image files and organize them by background number
    for file_name in os.listdir(source_dir):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            card_type, img_num = extract_image_info(file_name)
            if img_num is not None:
                background_groups[img_num].append(file_name)
    
    # Get unique background numbers and shuffle them
    background_numbers = list(background_groups.keys())
    random.shuffle(background_numbers)
    
    # Calculate split points for backgrounds
    total_backgrounds = len(background_numbers)
    n_train = int(total_backgrounds * train_ratio)
    n_val = int(total_backgrounds * val_ratio)
    
    # Split background numbers into train/val/test
    train_backgrounds = background_numbers[:n_train]
    val_backgrounds = background_numbers[n_train:n_train + n_val]
    test_backgrounds = background_numbers[n_train + n_val:]
    
    # Dictionary to store statistics
    stats = defaultdict(lambda: defaultdict(int))
    
    # Function to copy files and update statistics
    def copy_files_for_backgrounds(backgrounds, target_dir, split_name):
        for bg_num in backgrounds:
            for file_name in background_groups[bg_num]:
                card_type, _ = extract_image_info(file_name)
                shutil.copy2(
                    os.path.join(source_dir, file_name),
                    os.path.join(target_dir, file_name)
                )
                stats[card_type][split_name] += 1
                stats['total'][split_name] += 1
    
    # Copy files to respective directories
    copy_files_for_backgrounds(train_backgrounds, train_dir, 'train')
    copy_files_for_backgrounds(val_backgrounds, val_dir, 'val')
    copy_files_for_backgrounds(test_backgrounds, test_dir, 'test')
    
    # Print statistics
    print("\nBackground split:")
    print(f"Train backgrounds: {len(train_backgrounds)} ({len(train_backgrounds)/total_backgrounds:.1%})")
    print(f"Validation backgrounds: {len(val_backgrounds)} ({len(val_backgrounds)/total_backgrounds:.1%})")
    print(f"Test backgrounds: {len(test_backgrounds)} ({len(test_backgrounds)/total_backgrounds:.1%})")
    
    print("\nDetailed statistics per card type:")
    for card_type in stats:
        if card_type != 'total':
            total_card = sum(stats[card_type].values())
            print(f"\nCard type: {card_type}")
            print(f"Train: {stats[card_type]['train']} ({stats[card_type]['train']/total_card:.1%})")
            print(f"Validation: {stats[card_type]['val']} ({stats[card_type]['val']/total_card:.1%})")
            print(f"Test: {stats[card_type]['test']} ({stats[card_type]['test']/total_card:.1%})")
    
    print("\nOverall Statistics:")
    total = stats['total']['train'] + stats['total']['val'] + stats['total']['test']
    print(f"Total files in train: {stats['total']['train']} ({stats['total']['train']/total:.1%})")
    print(f"Total files in validation: {stats['total']['val']} ({stats['total']['val']/total:.1%})")
    print(f"Total files in test: {stats['total']['test']} ({stats['total']['test']/total:.1%})")

def main():
    # Define paths
    base_dir = "images"  # Your base directory
    source_dir = os.path.join(base_dir, "cards_with_backgrounds")
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "valid")
    test_dir = os.path.join(base_dir, "test")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Split the dataset
    split_dataset(source_dir, train_dir, val_dir, test_dir, train_ratio=0.7, val_ratio=0.1)

if __name__ == "__main__":
    main()