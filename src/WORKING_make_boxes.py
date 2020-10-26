# Richard Kuzma, October 2020
# tutorial: https://medium.com/analytics-vidhya/optical-character-recognition-ocr-using-py-tesseract-part-1-29ba8104eb2b
# kylo_ren OERs are .png

# note on jupyter notebook env troubles
# python -m ipykernel install --user --name ENVNAM --display-name "WHAT DISPLAYS IN JUPYTER NOTEBOOK KERNEL SELECTION"

import os, sys
sys.path.append('/usr/local/Cellar/tesseract/4.1.1/bin/')
# # tesseract must be in your PATH or include this line with path to tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from PIL import Image, ImageSequence


def make_boxes(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    print(d.keys())

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(np.array(img), (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img

def write_text_to_file(img, filename: str, output_path='../data/outputs/'):
    with open(output_path+filename, 'w') as outfile:
        outfile.write(pytesseract.image_to_string(img))

def show_boxes(img):
    img_box = make_boxes(img)
    print('press any key to exit')
    cv2.imshow('img with bounding boxes', img_box)
    cv2.waitKey(0)


### main
def main():
    # load image
    if len(sys.argv) < 2:
        print('enter a file to read and convert to text')
        pass
    else:
        args = sys.argv[1:]
        IMG_PATH = '../data/images/'
        OUTPUT_PATH = '../data/outputs/'
        for arg in args:
            img_filename= str(arg)
            img_name = img_filename[0:img_filename.index('.')]
            img_ext = img_filename[img_filename.index('.'):]
            print('reading: ' + img_filename)
            print('from: ' + IMG_PATH)
            print('name: ' + img_name)
            print('ext: ' + img_ext)
            img = Image.open(IMG_PATH + img_filename)

            # write text to file with pytesseract
            write_text_to_file(img, OUTPUT_PATH + img_name+'.txt')


if __name__ == "__main__" :
    main()



    # cv2.imshow('img', img)
    # cv2.waitKey(0)












# text = pytesseract.image_to_string(img)
# print(text)

# print('\n\n\n\n')
# data = pytesseract.image_to_data(img)
# print(data)

### functions from nanonets.com/blog/ocr-with-tesseractandopencv
# get grayscale image
# def get_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # noise removal
# def remove_noise(image):
#     return cv2.medianBlur(image,5)
#
# #thresholding
# def thresholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#
# #dilation
# def dilate(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.dilate(image, kernel, iterations = 1)
#
# #erosion
# def erode(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.erode(image, kernel, iterations = 1)
#
# #opening - erosion followed by dilation
# def opening(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
# #canny edge detection
# def canny(image):
#     return cv2.Canny(image, 100, 200)
#
# #skew correction
# def deskew(image):
#     coords = np.column_stack(np.where(image > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return rotated
#
# #template matching
# def match_template(image, template):
#     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
#
# ### function from somewhere else
# def mark_region(image_path):
#
#     im = cv2.imread(image_path)
#
#     gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (9,9), 0)
#     thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
#
#     # Dilate to combine adjacent text contours
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
#     dilate = cv2.dilate(thresh, kernel, iterations=4)
#
#     # Find contours, highlight text areas, and extract ROIs
#     cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
#     line_items_coordinates = []
#     for c in cnts:
#         area = cv2.contourArea(c)
#         x,y,w,h = cv2.boundingRect(c)
#         print('area: {}'.format(area))
#         print('x: {}'.format(x))
#         print('y: {}'.format(y))
#         print('h: {}'.format(w))
#         print('w: {}'.format(h))
#
#         if y >= 600 and x <= 1000:
#             if area > 10000:
#                 image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
#                 line_items_coordinates.append([(x,y), (2200, y+h)])
#
#         if y >= 2400 and x<= 2000:
#             image = cv2.rectangle(im, (x,y), (2200, y+h), color=(255,0,255), thickness=3)
#             line_items_coordinates.append([(x,y), (2200, y+h)])
#
#
#     return image, line_items_coordinates


# new_img, img_coords = mark_region(img_path)
# img.show()
# new_img.show()
# print('img_coords length: {}'.format(len(img_coords)))
# for i in img_coords:
#     print(i)
