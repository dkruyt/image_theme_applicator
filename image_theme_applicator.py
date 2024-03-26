from PIL import Image
import numpy as np
import argparse
import yaml

def hex_to_rgb(hex_color):
    # Convert hex color code to RGB tuple
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def closest_color(rgb, theme_colors):
    # Calculate the distance to each theme color and return the closest
    distances = np.sqrt(np.sum((theme_colors - rgb)**2, axis=1))
    return theme_colors[np.argmin(distances)]

def apply_theme(image_path, theme_path, output_path):
    # Load the theme colors from the YAML file
    with open(theme_path, 'r') as file:
        theme_data = yaml.safe_load(file)
    theme_colors = np.array([hex_to_rgb(color) for color in theme_data.values()])
    
    # Load the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    # Convert image to NumPy array for faster processing
    data = np.array(img)
    
    # Reshape the data to a 2D array for vectorized operations
    flat_data = data.reshape(-1, 3)
    
    # Replace each pixel with the closest theme color
    new_flat_data = np.apply_along_axis(closest_color, 1, flat_data, theme_colors)
    
    # Reshape the data back to the original image shape
    new_data = new_flat_data.reshape(data.shape)
    
    # Convert array back to an image
    new_img = Image.fromarray(new_data.astype('uint8'), 'RGB')
    
    # Save the modified image
    new_img.save(output_path)

def main():
    parser = argparse.ArgumentParser(description='Apply a color theme to an image.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input image file')
    parser.add_argument('--output', type=str, required=True, help='Path to save the output image file')
    parser.add_argument('--theme', type=str, required=True, help='Path to the YAML file containing the theme colors')
    args = parser.parse_args()
    
    apply_theme(args.input, args.theme, args.output)

if __name__ == "__main__":
    main()