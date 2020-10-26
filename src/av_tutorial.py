# Richard Kuzma, October 2020
# tutorial: https://medium.com/analytics-vidhya/optical-character-recognition-ocr-using-py-tesseract-part-1-29ba8104eb2b

import pytesseract

import os, sys
sys.path.append('/usr/local/Cellar/tesseract/4.1.1/bin/')
# # tesseract must be in your PATH or include this line with path to tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

from PIL import Image

### clean image
# clean_image = Image.open('../data/ocr_test_clean.png')
# clean_image.show()
# text = pytesseract.image_to_string(clean_image)
# print(text + '\n')

### noisy image
# noisy_image = Image.open('../data/ocr_test_noisy.png')
# noisy_image.show()
# text = pytesseract.image_to_string(noisy_image)
# print(text + '\n')


### image resizing (slightly smaller here)
# # no noticable difference
# # original image
# img = Image.open('../data/ocr_test_noisy.png')
# print('width: {}'.format(img.size[0]))
# print('height: {}'.format(img.size[1]))
# img.show()
# print('img text:')
# print(pytesseract.image_to_string(img))
#
# # set the base width of our image
# basewidth = 600
# # get the correct aspect ratio, by taking the base width/actual width
# wpercent = (basewidth / float(img.size[0]))
#
# # With that ratio we can just get the appropriate height of the image.
# hsize = int((float(img.size[1]) * float(wpercent)))
#
# # Finally, lets resize the image. antialiasing is a specific way of resizing lines to try and make them
# # appear smooth
# print('\nresized.')
# resized_img = img.resize((basewidth, hsize), Image.ANTIALIAS)
# print('width: {}'.format(resized_img.size[0]))
# print('height: {}'.format(resized_img.size[1]))
# resized_img.show()
# print('resized_img text:')
# print(pytesseract.image_to_string(resized_img))

### grayscale image
# even worse
# grayscale_img = Image.open('../data/ocr_test_noisy.png')
# grayscale_img = grayscale_img.convert('L')
# grayscale_img.show()
# print(pytesseract.image_to_string(grayscale_img))

### binarization using PIL.Image.convert()
# # '1' is string parameter to do binarization
# bin_img = Image.open('../data/ocr_test_noisy.png').convert('1')
# bin_img.show()
# print(pytesseract.image_to_string(bin_img))

### custom binarize function
# note that 0 is black, 255 is white
# works really well for thresh = 64
def binarize(image_to_transform, threshold):
    # convert to grayscale
    output_image=image_to_transform.convert("L")
    for x in range(output_image.width):
        for y in range(output_image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            if output_image.getpixel((x,y))< threshold: #note that the first parameter is actually a tuple object
                output_image.putpixel( (x,y), 0 )
            else:
                output_image.putpixel( (x,y), 255 )
    return output_image


for thresh in range(0,257,64):
    print("Trying with threshold " + str(thresh))
    temp = binarize(Image.open('../data/ocr_test_noisy.png'), thresh)
    temp.show()
    print(pytesseract.image_to_string(temp))
    print('\n\n')














# end
