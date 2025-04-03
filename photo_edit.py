from PIL import Image, ImageEnhance, ImageFilter
import os

def apply_ghibli_effect(image_path, output_path):
    image = Image.open(image_path)
    image = image.filter(ImageFilter.DETAIL)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.5)
    image.save(output_path)

def apply_anime_effect(image_path, output_path):
    image = Image.open(image_path)
    image = image.filter(ImageFilter.CONTOUR)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    image.save(output_path)

def apply_cinematic_effect(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("L")  # Black & White
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.8)
    image.save(output_path)

def edit_photo(image_path, output_folder, edit_type):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    
    if edit_type == "ghibli":
        apply_ghibli_effect(image_path, output_path)
    elif edit_type == "anime":
        apply_anime_effect(image_path, output_path)
    elif edit_type == "cinematic":
        apply_cinematic_effect(image_path, output_path)
    else:
        return "Invalid edit type"
    
    return output_path
