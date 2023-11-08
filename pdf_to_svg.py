import os
from pdf2image import convert_from_path
import cairosvg
from PIL import Image

# Function to convert PDF to SVG and create tiles
def convert_pdf_to_svg_and_tile(pdf_path, output_folder, tile_size=(1280, 1280)):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path, fmt='png')

    # Convert each image to SVG and create tiles
    for i, image in enumerate(images):
        # Convert the image to SVG
        svg_bytes = cairosvg.png2svg(image.tobytes())
        
        # Save the SVG file
        svg_file = os.path.join(output_folder, f"page_{i+1}.svg")
        with open(svg_file, 'wb') as f:
            f.write(svg_bytes)

        print(f"Converted page {i+1} to SVG and saved as '{svg_file}'")

        # Create an image object from the SVG bytes and tile it
        img = Image.open(svg_file)
        tile(output_folder, img, f"page_{i+1}_tile", tile_size)

def tile(output_folder, image, prefix, tile_size):
    width, height = image.size

    for i in range(0, width, tile_size[0]):
        for j in range(0, height, tile_size[1]):
            box = (i, j, i + tile_size[0], j + tile_size[1])
            tile = image.crop(box)
            tile_path = os.path.join(output_folder, f"{prefix}_{i}_{j}.svg")
            tile.save(tile_path, "SVG")
            print(f"Saved tile {tile_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = 'example.pdf'  # Replace with your PDF file path
    output_folder = 'svg_output'  # Replace with your desired output folder
    convert_pdf_to_svg_and_tile(pdf_path, output_folder)
