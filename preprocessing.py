import cv2 as cv
import numpy as np
import pytesseract as pyt
import os

def preprocess_image(image_path):
    img = cv.imread(image_path)
    if img is None:
        raise ValueError("Image not found.")

    h, w = img.shape[:2]
    scale = max(h, w)

    bilateral_d = 1 if scale < 600 else 13
    median_k = 1 if scale < 600 else 15
    sharpen_amount = 1.5 if scale < 600 else 2.5
    sharpen_subtract =0.5  if scale < 600 else 1.5
    kernel_size = (1, 1) 

    blu = cv.bilateralFilter(img, bilateral_d, 75, 75)
    im = cv.addWeighted(img, sharpen_amount, blu, -sharpen_subtract, 0)

    blur = cv.medianBlur(im, median_k)
    sharpened = cv.addWeighted(img, sharpen_amount, blur, -sharpen_subtract, 0)

    kernel = np.ones(kernel_size, np.uint8)
    cleaned = cv.morphologyEx(sharpened, cv.MORPH_OPEN, kernel, iterations=1)
    cleaned = cv.morphologyEx(cleaned, cv.MORPH_CLOSE, kernel, iterations=1)

    return cleaned

def process_folder(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
           
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(input_dir, filename)
            try:
                processed = preprocess_image(path)
                out_path = os.path.join(output_dir, filename)
                cv.imwrite(out_path, processed)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def display(image, title='Image'):
    # Resize for display if needed
    display_img = cv.resize(image, (750, 750), interpolation=cv.INTER_AREA)  
    cv.imshow(title, display_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Example usage
image_path = "112_2.png"
processed = preprocess_image(image_path)
display(processed, 'Processed Image')
print(pyt.image_to_string(processed, lang='eng'))
im=cv.imread(image_path)
print(pyt.image_to_string(im,lang='eng'))
