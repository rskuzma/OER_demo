# Richard Kuzma, October 2020
# tutorial: https://medium.com/analytics-vidhya/optical-character-recognition-ocr-using-py-tesseract-part-1-29ba8104eb2b
# kylo_ren OERs are .png

# note on jupyter notebook env troubles
# python -m ipykernel install --user --name ENVNAM --display-name "WHAT DISPLAYS IN JUPYTER NOTEBOOK KERNEL SELECTION"

import os, sys
import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageSequence

### tesseract must be in your PATH or teseseract_cmd needs a path to it
# # if using on local machine
# sys.path.append('/usr/local/Cellar/tesseract/4.1.1/bin/')
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# for heroku deployment (also going to add to oer_demo.py)
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

from pytesseract import Output




def write_text_to_file(img, filename: str, output_path='./data/text/', page = ''):
    with open(output_path+filename + '.txt', 'a') as outfile:
        print('opening file: ' + output_path + filename + '.txt')
        outfile.write(pytesseract.image_to_string(img))
        print('used pytesseract to write image to string and appended to file')
        outfile.write('\n')
        if page != '':
            outfile.write('===== END OF ' + page.upper() + ' =====')
            outfile.write('\n\n')

    print('finished ' + page)


### main
def main():
    # load image
    if len(sys.argv) < 2:
        print('enter a file to read and convert to text')
        pass
    else:
        args = sys.argv[1:]
        IMG_PATH = './data/images/'
        OUTPUT_PATH = './data/text/'
        for arg in args:
            print('\n')
            img_filename = arg
            img_name = img_filename[0:(img_filename.index('page')-1)]
            img_page = img_filename[img_filename.index('page'):(img_filename.index('page')+5)]
            img_ext = img_filename[img_filename.index('.'):]
            print('image_filename: ' + img_filename)
            print('IMG_PATH: ' + IMG_PATH)
            print('img_name: ' + img_name)
            print('img_page: ' + img_page)
            print('img_ext: ' + img_ext)
            img = Image.open(IMG_PATH + img_filename)

            # write text to file with pytesseract
            write_text_to_file(img, filename=img_name, output_path='./data/text/', page = img_page)
        print('\nfinished all pages')

if __name__ == "__main__" :
    main()
