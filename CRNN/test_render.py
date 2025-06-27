from PIL import ImageFont, Image, ImageDraw

# Define the font path
font_path = 'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/fonts/Arial.ttf'

try:
    # Load the font
    font = ImageFont.truetype(font_path, size=32)
    print(f"Font loaded successfully: {font_path}")

    # Create a new image
    img = Image.new('RGB', (200, 50), color='white')
    d = ImageDraw.Draw(img)

    # Draw the text
    d.text((10, 10), 'Climate', font=font, fill='black')

    # Save the image
    img.save('C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic/en/test_render.png')
    print('Test image saved as test_render.png')

except Exception as e:
    print(f"Error: {e}")