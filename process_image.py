from PIL import Image
import os
import shutil

# Define paths
source_image = os.path.join('img_src', 'muscle-car-retro-vintage-car-sunset-neon-5k-3840x2160-1229.jpg')
static_images_dir = os.path.join('CarFleetManagement', 'static', 'images')

# Create target paths
color_image_path = os.path.join(static_images_dir, 'hero-retro-car.jpg')
bw_image_path = os.path.join(static_images_dir, 'hero-retro-car-bw.jpg')

# Ensure the directory exists
os.makedirs(static_images_dir, exist_ok=True)

# Process the color image (resize to be web-friendly)
img = Image.open(source_image)
# Resize to a more web-friendly size while maintaining aspect ratio
width, height = img.size
new_width = 1200
new_height = int(height * (new_width / width))
resized_img = img.resize((new_width, new_height), Image.LANCZOS)
resized_img.save(color_image_path, optimize=True, quality=85)
print(f"Created color image: {color_image_path}")

# Create black and white version
bw_img = resized_img.convert('L')  # Convert to grayscale
bw_img.save(bw_image_path, optimize=True, quality=85)
print(f"Created black and white image: {bw_image_path}")

print("Image processing complete!")