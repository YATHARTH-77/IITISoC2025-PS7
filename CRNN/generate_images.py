from trdg.generators import GeneratorFromStrings
import os
import logging
from PIL import ImageFont, Image, ImageDraw

logging.basicConfig(filename='generate_images.log', level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

languages = {
    'en': 'Arial.ttf',
    'es': 'Arial.ttf',
    'hi': 'NotoSans-Devanagari.ttf',
    'zh': 'NotoSansSC-Regular.ttf',
    'ar': 'NotoSans-Arabic.ttf'
}
font_dir = 'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/fonts'
os.makedirs('C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic', exist_ok=True)
for lang in languages:
    file_path = f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/oscar/oscar_{lang}_clean.txt'
    font_path = f'{font_dir}/{languages[lang]}'
    if not os.path.exists(font_path):
        logger.error(f"Font not found: {font_path}")
        print(f"Error: Font not found for {lang}: {font_path}")
        continue
    try:
        font = ImageFont.truetype(font_path, size=32)
        print(f"Font loaded successfully for {lang}: {font_path}")
    except OSError as e:
        logger.error(f"Failed to load font for {lang}: {font_path}, Error: {str(e)}")
        print(f"Error: Failed to load font for {lang}: {font_path}, Error: {str(e)}")
        continue
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        logger.warning(f"{file_path} is empty or missing")
        print(f"Warning: {file_path} is empty or missing")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]
    if not texts:
        logger.warning(f"No texts found in {file_path}")
        print(f"No texts found in {file_path}")
        continue
    print(f"Processing {len(texts[:100])} texts for {lang}: {texts[:5]}")
    generator = GeneratorFromStrings(
        strings=texts[:25000],
        count=25000,
        fonts=[font_path],
        size=32,
        language=lang,
        background_type=0,
        text_color='#000000',
        image_dir=f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic/{lang}',
        fit=True  # Dynamic sizing to fit text
    )
    os.makedirs(f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic/{lang}', exist_ok=True)
    for i, (img, lbl) in enumerate(generator):
        # Load font for dynamic sizing
        draw = ImageDraw.Draw(img)
        text_width = draw.textlength(lbl, font=font)
        # Get bounding box to calculate full height including descenders
        bbox = font.getbbox(lbl)
        text_height = bbox[3] - bbox[1]  # Height = bottom - top
        # Dynamic padding: Add 20% of text width and 20% of text height as minimum padding
        new_width = int(img.width + text_width * 0.2 + 10)
        new_height = int(img.height + text_height * 0.3 + 30)
        # Custom wrapper with dynamic padding
        img_with_padding = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_with_padding.save(f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic/{lang}/img_{i}.png')
        with open(f'C:/Users/YATHARTH MAURYA/Desktop/PS-7/IITISoC2025-PS9/data/synthetic/{lang}/labels.txt', 'a', encoding='utf-8') as f:
            f.write(f'img_{i}.png\t{lbl}\n')
    logger.info(f"Generated {len(texts[:25000])} images for {lang}")
    print(f"Generated {len(texts[:25000])} images for {lang}")