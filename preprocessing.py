'''
main features in preprocessing
inverting(not that useful)
rescaling
binarization
noise reduction(dilation, erosion, morphologyEx, median blur) 
rotating
removing borders
'''
import cv2 as cv
import numpy as np
import pytesseract as pyt
import os
image_path='page_01.jpg'
def preprocess_image(image_path):

    # Load the image
    img = cv.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to load.")

    # grayscaling
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # binarization
    threshold,thresh=cv.threshold(gray, 205, 225, cv.THRESH_BINARY)
    def remove_noise(image):
        kernel= np.ones((1, 1), np.uint8)
        image=cv.dilate(image, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        image=cv.erode(image, kernel, iterations=1)
        image=cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
        image=cv.medianBlur(image, 3)
        return image
    im=remove_noise(thresh)
    return im

def process_folder(input_dir, output_dir,):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(input_dir, filename)
            processed = preprocess_image(path) 
            out_path = os.path.join(output_dir, filename)
            cv.imwrite(out_path, processed) 

def display(image, title='Image'):
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyAllWindows()    
x=preprocess_image(image_path)
display(x)
result=pyt.image_to_string(x)
print(result)
