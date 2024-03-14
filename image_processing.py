from PIL import Image
import os
from typing import Tuple

supported_input_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']

def resize_stretch(image_path: str, output_size: Tuple[int, int]) -> None:
    with Image.open(image_path) as img:
        img = img.resize(output_size, Image.Resampling.LANCZOS)
        img.save(get_new_filename(image_path, "stretched"))

def resize_crop(image_path: str, output_size: Tuple[int, int]) -> None:
    with Image.open(image_path) as img:
        target_ratio = output_size[0] / output_size[1]
        image_ratio = img.width / img.height

        if image_ratio > target_ratio:
            new_width = int(target_ratio * img.height)
            left = (img.width - new_width) / 2
            img = img.crop((left, 0, left + new_width, img.height))
        elif image_ratio < target_ratio:
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) / 2
            img = img.crop((0, top, img.width, top + new_height))

        img = img.resize(output_size, Image.Resampling.LANCZOS)
        img.save(get_new_filename(image_path, "cropped"))

def get_new_filename(original_path: str, suffix: str) -> str:
    file_dir, file_name = os.path.split(original_path)
    name, ext = os.path.splitext(file_name)
    new_name = f"{name}_{suffix}{ext}"
    return os.path.join(file_dir, new_name)

def image_to_format(image_file_path: str, output_format: str = 'ICO') -> None:
    with Image.open(image_file_path) as img:
        if output_format == 'ICO':
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
    
        output_file_path = os.path.splitext(image_file_path)[0] + '.' + output_format.lower()
        img.save(output_file_path, format=output_format)

    print(f"Converted {image_file_path} to {output_file_path}")

def image_converter() -> None:
    print("\nImage Converter")
    output_format = input("Enter the desired output format (ICO, JPEG, BMP, GIF, PNG, WEBP): ").upper()
    supported_formats = ['ICO', 'JPEG', 'BMP', 'GIF', 'PNG', 'WEBP']
    
    if output_format not in supported_formats:
        print("Unsupported format. Please choose from ICO, JPEG, BMP, GIF, PNG, or WEBP.")
        return
    
    eligible_files = [filename for filename in os.listdir(os.getcwd()) if os.path.splitext(filename)[1].lower() in supported_input_formats]
    for filename in eligible_files:
        image_to_format(filename, output_format)

def image_resizer() -> None:
    print("\nImage Resizer")
    print("Choose a mode: \n1- Stretch\n2- Crop")
    mode = input("Enter mode (1 or 2): ")
    width, height = map(int, input("Enter the desired size in pixels (width height): ").split())

    resize_function = resize_stretch if mode == '1' else resize_crop
    picture_files = [file for file in os.listdir() if file.lower().endswith(tuple(supported_input_formats)) and "_stretched" not in file.lower() and "_cropped" not in file.lower()]

    for picture in picture_files:
        resize_function(picture, (width, height))
        print(f"Resized {picture} and saved as a new file.")

if __name__ == "__main__":
    print("Choose an option:\n1- Image Resizer\n2- Image Converter")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        image_resizer()
    elif choice == '2':
        image_converter()
    else:
        print("Invalid choice. Please enter 1 or 2.")