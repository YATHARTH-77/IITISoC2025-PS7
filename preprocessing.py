import cv2 as cv
import numpy as np
import pytesseract as pyt
import os

def preprocess_image(image_path):
    # Load the image
    img = cv.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to load.")

    # Convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce high-frequency noise
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(
        blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY_INV, 11, 2
    )
    
    
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)
    
    
    def remove_small_dots(image):
        # Find all connected components
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
            image, connectivity=8
        )
        
        
        output = np.zeros_like(image)
        
       
        min_size = 20
        
        for i in range(1, num_labels):
            # Skip small components
            if stats[i, cv.CC_STAT_AREA] >= min_size:
                # Add large components to output
                output[labels == i] = 255
                
        return output
    
    
    cleaned = remove_small_dots(cleaned)
    
    
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv.dilate(cleaned, kernel, iterations=1)
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
    
    display_img = cv.resize(image, (750, 750), interpolation=cv.INTER_AREA)  
    cv.imshow(title, display_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Example 
image_path = "page_01.jpg"
processed = preprocess_image(image_path)
display(processed, 'Processed Image')
print(pyt.image_to_string(processed, lang='eng'))
