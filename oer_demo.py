
### Imports
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import os, sys, json
import pandas as pd
import streamlit as st
from PIL import Image, ImageSequence
# import pypdf2
# from pdf2image import convert_from_path, convert_from_bytes
# # will need poppler installed for pdf2image to work
# sys.path.append(os.path.join('/usr/local/Cellar/poppler/'))

# for local
# sys.path.append('/usr/local/Cellar/tesseract/4.1.1/bin/')
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# for heroku (also going to add to oer_demo.py)
# pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

# .py files
sys.path.append(os.path.join('./data/images/'))
sys.path.append(os.path.join('./src/'))
import parse_pdf_67_10_1
import parse_pdf_67_10_2
import pdf_to_text
# import parse_tiff_67_9_2011
import binarize_images
# import img_to_text
# import remove_whitespace


STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

FILE_TYPES = ["png", "jpg", "tiff"]


class FileType(Enum):
    """Used to distinguish between file types"""

    IMAGE = "Image"
    CSV = "csv"
    PYTHON = "Python"


def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    """The file uploader widget does not provide information on the type of file uploaded so we have
    to guess using rules or ML

    I've implemented rules for now :-)

    Arguments:
        file {Union[BytesIO, StringIO]} -- The file uploaded

    Returns:
        FileType -- A best guess of the file type
    """

    if isinstance(file, BytesIO):
        return FileType.IMAGE
    content = file.getvalue()
    if (
        content.startswith('"""')
        or "import" in content
        or "from " in content
        or "def " in content
        or "class " in content
        or "print(" in content
    ):
        return FileType.PYTHON

    return FileType.CSV


def main():
    # st.write(os.getcwd())
    st.markdown('''
    # Making Officer Evaluation Reports Machine-Readable
    1LT Richard Kuzma, Army AI Task Force, NOV2020
    ### Value to the Army
    - OERs are images or PDFs. Readable by humans, not machines
    - Structured, machine-readable data can be better organized, stored, and analyzed

    ### How this works
    - Input an OER in PDF form
    - Use PDFPlumber, a python library, to read document text
    - Use a custom-made script to make sense of the text
    - Save the text to a JSON file

    ### Caveats
    - Works on new OER formats (DA Form 67-10-1 and 67-10-2 as PDFs)
    - This demo is on a local machine (not publicly accessible)
    - Text parsing is brittle. This may not work for all PDFs

    ''')


    IMG_PATH = './data/images/'
    PDF_PATH = './data/pdf/'
    TXT_PATH = './data/text/'
    OUTPUT_PATH = './data/output/'

    img_filename = ''
    img_ext = ''
    IMG_UPLOADED = False
    PDF_UPLOADED = False

    # st.info(__doc__)
    st.markdown(STYLE, unsafe_allow_html=True)

    ### get last name for file saving
    last_name_input = st.text_input("Enter your last name")
    if not last_name_input:
        st.warning('Please type last name and hit enter')
    last_name = last_name_input.lower()

    ### select threshold for binarizing
    # threshold_input = st.number_input("Enter threshold for binarizing images [0, 255]", min_value=0, max_value=255, value=150)
    # thresh = str(threshold_input)

    upload_type = st.radio('Select OER type:', ['Post-2014 (Company Grade) (DA Form 67-10-1)', 'Post-2014 (Field Grade) (DA Form 67-10-2)'])#, 'Pre-2014 (Company Grade) (DA Form 67-9)'])
    warning = st.empty()


    ### file upload
    # .tiff (2 pg)
    if upload_type == 'Post-2014 (Field Grade) (DA Form 67-10-2)':
        upload = st.file_uploader("Upload 2 page pdf", type="pdf")
        if not upload:
            warning.info("Please upload 2 pg .pdf file")
        if upload:
            upload_full_name = upload.name
            upload_name = upload_full_name[:upload_full_name.rindex('.')]
            ext = upload_full_name[upload_full_name.rindex('.'):]
            bin_filename = last_name + '.bin'
            txt_filename = last_name + '.txt'
            json_filename = last_name + '.json'

            # st.write('upload full name: ' + upload_full_name)
            # st.write('name: ' + upload_name)
            # st.write('extension: ' + ext)
            # st.write('upload type: {}'.format(type(upload)))
            # st.write('upload.read() type: {}'.format(type(upload.read())))

            with open(PDF_PATH + bin_filename, 'wb') as f:
                # st.write('tell: {}'.format(upload.tell()))
                # st.write('seek: {}'.format(upload.seek(0)))
                # st.write('tell again: {}'.format(upload.tell()))
                f.write(upload.read())

            with st.spinner('Converting pdf to text...'):
                sys.argv = ["pdf_to_text.py", bin_filename, last_name, 'true']
                pdf_to_text.main()

            with st.spinner('Reading pdf text to json'):
                sys.argv = ["parse_pdf_67_10_2.py", last_name + '.txt']
                parse_pdf_67_10_2.main()

            with open('./data/output/' + last_name + '.json', 'r') as f:
                output = json.load(f)
            st.write(output)

###################################################
    elif upload_type == 'Post-2014 (Company Grade) (DA Form 67-10-1)':
        upload = st.file_uploader("Upload 2 page pdf", type="pdf")
        if not upload:
            warning.info("Please upload 2 pg .pdf file")
        if upload:
            upload_full_name = upload.name
            upload_name = upload_full_name[:upload_full_name.rindex('.')]
            ext = upload_full_name[upload_full_name.rindex('.'):]
            bin_filename = last_name + '.bin'
            txt_filename = last_name + '.txt'
            json_filename = last_name + '.json'

            # st.write('upload full name: ' + upload_full_name)
            # st.write('name: ' + upload_name)
            # st.write('extension: ' + ext)
            # st.write('upload type: {}'.format(type(upload)))
            # st.write('upload.read() type: {}'.format(type(upload.read())))

            with open(PDF_PATH + bin_filename, 'wb') as f:
                # st.write('tell: {}'.format(upload.tell()))
                # st.write('seek: {}'.format(upload.seek(0)))
                # st.write('tell again: {}'.format(upload.tell()))
                f.write(upload.read())

            with st.spinner('Converting pdf to text...'):
                sys.argv = ["pdf_to_text.py", bin_filename, last_name, 'true']
                pdf_to_text.main()

            with st.spinner('Reading pdf text to json'):
                sys.argv = ["parse_pdf_67_10_1.py", last_name + '.txt']
                parse_pdf_67_10_1.main()

            with open('./data/output/' + last_name + '.json', 'r') as f:
                output = json.load(f)
            st.write(output)

###################################################
    # elif upload_type == 'Pre-2014 (Company Grade) (DA Form 67-9)':
    #     upload = st.file_uploader("Upload 2 page tif", type=["tiff", "tif", "jpeg"])
    #     if not upload:
    #         warning.info("Please upload 2 pg .tiff file")
    #     if upload:
    #         upload_full_name = upload.name
    #         upload_name = upload_full_name[:upload_full_name.rindex('.')]
    #         ext = upload_full_name[upload_full_name.rindex('.'):]
    #         bin_filename = last_name + '.bin'
    #         txt_filename = last_name + '.txt'
    #         stripped_txt_filename = last_name + '_stripped.txt'
    #         json_filename = last_name + '.json'
    #
    #         st.write('upload full name: ' + upload_full_name)
    #         st.write('name: ' + upload_name)
    #         st.write('extension: ' + ext)
    #         st.write('upload type: {}'.format(type(upload)))
    #         st.write('upload.read() type: {}'.format(type(upload.read())))
    #
    #         # split the image
    #         img = Image.open(upload)
    #         st.write('img is type: {}'.format(type(img)))
    #         for i, page in enumerate(ImageSequence.Iterator(img)):
    #             temp = IMG_PATH + last_name + "_page{}".format(i+1) + ext
    #             st.write('path: ' + temp)
    #             page.save(temp)
    #             st.write('check for save on page {}'.format(i+1))
    #
    #
    #         filename_page_1 = last_name + '_page1' + ext
    #         filename_page_2 = last_name + '_page2' + ext
    #         st.write('filenames: ' + filename_page_1 + ' and ' + filename_page_2)
    #
    #         # binarized images new file names
    #         filename_bin_page_1 = last_name + '_bin_' + thresh + '_page1' + ext
    #         filename_bin_page_2 = last_name + '_bin_' + thresh + '_page2' + ext
    #         st.write('bin filenames: ' + filename_bin_page_1 + ' and ' + filename_bin_page_2)
    #
    #
    #         with st.spinner('Preprocessing OER image'):
    #             sys.argv = ["binarize_images.py", thresh, filename_page_1, filename_page_2]
    #             # os.system('python binarize_images 150' + page1_name + ' ' + page2_name)
    #             binarize_images.main()
    #
    #         ### img to text
    #         with st.spinner('Reading text from image...'):
    #             sys.argv = ["img_to_text.py", filename_bin_page_1, filename_bin_page_2]
    #             img_to_text.main()
    #
    #         ### remove whitespace
    #         with st.spinner('Removing whitespace from txt file...'):
    #             sys.argv = ["remove_whitespace.py", txt_filename]
    #             remove_whitespace.main()
    #         st.success('Whitespace removed!')
    #
    #         ### parse
    #         with st.spinner('Converting text to machine-readable format...'):
    #             sys.argv = ["parse_tiff_67_9_2011.py", stripped_txt_filename]
    #             parse_tiff_67_9_2011.main()
    #         st.success('Conversion complete!')
    #
    #         ### display output
    #         st.write('## Output')
    #         with open('./data/output/' + json_filename, 'r') as f:
    #             output = json.load(f)
    #         st.write(output)

#########################

main()
