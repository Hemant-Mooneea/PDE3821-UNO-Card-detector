import os
import shutil
from pathlib import Path

def organize_uno_cards(source_folder, output_folder):
    # Create Path objects
    source_path = Path(source_folder)
    output_path = Path(output_folder)
    
    # Debug prints
    print(f"\nDebug Information:")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Source path absolute: {source_path.absolute()}")
    print(f"Source path exists: {source_path.exists()}")
    print(f"Source path is directory: {source_path.is_dir()}")
    
    # List all files in the directory
    print("\nFiles in source directory:")
    for file in source_path.iterdir():
        print(f"- {file.name} (is file: {file.is_file()})")
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all PNG files (case insensitive)
    png_files = list(source_path.glob('*.[pP][nN][gG]'))
    
    if not png_files:
        print("\nNo PNG files found in the source directory!")
        return
    
    # Track files per prefix for summary
    prefix_counts = {}
    
    for file_path in png_files:
        try:
            filename = file_path.stem
            # Handle "+4" and "wild" cases based on the start of the filename
            if filename.startswith("+4"):
                prefix = "+4"
            elif filename.startswith("wild"):
                prefix = "wild"
            else:
                # Extract prefix based on color and number only (ignore extra suffixes)
                parts = filename.split('_')
                prefix = f"{parts[0]}_{parts[1]}" if len(parts) >= 2 else filename

            # Create the folder for this prefix if it doesn't exist
            prefix_dir = output_path / prefix
            prefix_dir.mkdir(exist_ok=True)
            prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
            dest_path = prefix_dir / file_path.name
            shutil.copy2(file_path, dest_path)
            print(f"Copied: {file_path.name} -> {prefix}/{file_path.name}")
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
    
    print("\nOrganization complete! Summary:")
    total_files = sum(prefix_counts.values())
    print(f"Total files processed: {total_files}")
    print("\nFiles per category:")
    for prefix, count in sorted(prefix_counts.items()):
        print(f"- {prefix}: {count} files")
    
    print(f"\nOrganized files can be found in: {output_path}")

if __name__ == "__main__":
    source_folder = "images/cards_with_backgrounds"
    output_folder = "images/organized_cards"
    
    try:
        organize_uno_cards(source_folder, output_folder)
    except Exception as e:
        print(f"An error occurred: {e}")
