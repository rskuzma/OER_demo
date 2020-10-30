
### Imports
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import os, sys, json
import pandas as pd
import streamlit as st
from PIL import Image

# for heroku (also going to add to oer_demo.py)
# pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

# .py files
sys.path.append(os.path.join('./data/images/'))
sys.path.append(os.path.join('./src/'))
import parse
import binarize_images
import img_to_text

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
    st.write(os.getcwd())
    st.write('# OER image to text')
    # st.info(__doc__)
    st.markdown(STYLE, unsafe_allow_html=True)

    last_name_input = st.text_input("Enter your last name")
    if not last_name_input:
        st.warning('Please type last name and hit enter')

    threshold_input = st.number_input("Enter threshold for binarizing images [0, 255]", min_value=0, max_value=255, value=150)


    page1 = st.file_uploader("Upload OER page 1", type=FILE_TYPES)
    page2 = st.file_uploader("Upload OER page 2", type=FILE_TYPES)
    show_page1 = st.empty()
    show_page2 = st.empty()


    if not page1:
        show_page1.info("Please OER page 1 of type: " + ", ".join(FILE_TYPES))
        return
    if not page2:
        show_page2.info("Please upload OER page 2 of type: " + ", ".join(FILE_TYPES))
        return
    # get data from images



    # once both files uploaded
    if page1 and page2:
        show_page1.image(page1.read())
        show_page2.image(page2.read())
        # get names and extensions
        input1_filename = page1.name
        input1_ext = input1_filename[input1_filename.rindex('.')+1:]
        input2_filename = page2.name
        input2_ext = input2_filename[input2_filename.rindex('.')+1:]

        last_name = last_name_input.lower()

        # images new file names
        filename_page_1 = last_name + '_page1.' + input1_ext
        filename_page_2 = last_name + '_page2.' + input2_ext

        # binarized images new file names
        filename_bin_page_1 = last_name + '_bin_' + str(threshold_input) + '_page1.' + input1_ext
        filename_bin_page_2 = last_name + '_bin_' + str(threshold_input) + '_page2.' + input2_ext
            # filename_bin_page_1=$name$bin$thresh$page1$extension
            # filename_bin_page_2=$name$bin$thresh$page2$extension

        # txt filename
        txt_filename = last_name + '_bin_' + str(threshold_input) + '.txt'
            #txt_filename=$name$bin$thresh$txt

        # json file name
        json_filename = last_name + '_bin_' + str(threshold_input) + '.json'

        # open and save images to file structure
        page1_img = Image.open(page1)
        page2_img = Image.open(page2)

        SAVE_PATH = './data/images/'

        page1_img.save(SAVE_PATH + filename_page_1)
        page2_img.save(SAVE_PATH + filename_page_2)



        # page1.close()
        # page2.close()
        # if show:
        #     page_1_image_show = Image.open(SAVE_PATH + filename_page_1)
        #     page_2_image_show = Image.open(SAVE_PATH + filename_page_1)
        #     show_page1.image(page_1_image_show)
        #     show_page2.image(page_2_image_show)
        #     # show_page1.image(page1.read())
        #     # show_page2.image(page2.read())

        ### binarize
        with st.spinner('Preprocessing OER image'):
            sys.argv = ["binarize_images.py", str(threshold_input), filename_page_1, filename_page_2]
            # os.system('python binarize_images 150' + page1_name + ' ' + page2_name)
            binarize_images.main()


        ### img to text
        with st.spinner('Reading text from image...'):
            sys.argv = ["img_to_text.py", filename_bin_page_1, filename_bin_page_2]
            img_to_text.main()

        ### parse
        with st.spinner('Converting text to machine-readable format...'):
            sys.argv = ["parse.py", txt_filename, filename_bin_page_2]
            parse.main()
        st.success('Conversion complete!')


        st.write('## Output')

        with open('./data/output/' + json_filename, 'r') as f:
            output = json.load(f)
        st.write(output)











main()


#     if uploaded_file == None:
#         st.warning('Please upload pdf resume for the demo')
#         st.stop()
#     else:
#         if isinstance(file, BytesIO):
#             return FileType.IMAGE
#              = uploaded_pdf_to_text(uploaded_file)
#
#              show_file.image(file)
#
#
#
#
# file_option = st.selectbox('txt or pdf resume?', ['Select one', '.txt', '.pdf', 'upload my own pdf'])
# #### text options
# if file_option == 'Select one':
#     st.warning('Please select a .txt or .pdf example resume or upload your own pdf')
#     st.stop()
#
# elif file_option == '.txt':
#     option = st.selectbox('which .txt resume would you like to use?',
#                             ('Select one', 'Accounting', 'Data_Scientist', 'Logistics', 'Manufacturing_Engineer', 'Marketing', 'Nurse', 'Security_Guard', 'Software_Developer', 'Waitress'))
#     if option == 'Select one':
#         st.warning('Please select an example pdf resume for the demo')
#         st.stop()
#     text_lookup_res = load_from_txt(option.lower())
#
# ### pdf options
# elif file_option == '.pdf':
#     option = st.selectbox('which pdf resume would you like to use?',
#                             ('Select one', 'Accountant', 'Auditor', 'Banking_Analyst', 'Business_Associate', 'Compliance', 'Investment_Banking', 'Investor_Relations', 'Office_Manager', 'Paralegal'))
#     if option == 'Select one':
#         st.warning('Please select an example pdf resume for the demo')
#         st.stop()
#     pdf_to_text(option.lower())
#     text_lookup_res = load_from_txt(option.lower(), pdf=True)
#
# elif file_option == 'upload my own pdf':
#     uploaded_file = st.file_uploader("Choose a file", type='pdf')
#     if uploaded_file == None:
#         st.warning('Please upload pdf resume for the demo')
#         st.stop()
#     else:
#         text_lookup_res = uploaded_pdf_to_text(uploaded_file)
#         option = 'Uploaded'
#
# st.write('## {} Resume Text:'.format(option))
# st.write(text_lookup_res)
#
#
# ### Compute skill topics
# with st.spinner('Computing skills and job matches...'):
#     df = load_df()
#     d2v_model = load_d2v_model()
#     lda_model = load_LDA_model()
#     topic_words_all = load_topic_words()
# st.success('Computation complete.')
#
#
# section_separator()
# st.write('## {} Resume Skills:'.format(option))
# skill_words = 15
# topic_words = [topic_words_all[i][:skill_words] for i in range(len(topic_words_all))]
# with st.spinner('Extracting skills from resume...'):
#     res_topics = get_doc_topics(text_lookup_res, lda_model)
#     # st.write('Res topics ' + str(res_topics))
#     # st.write('Ordered res topics ' + str(res_topics_ordered))
#
# skills_to_display = st.slider('How many skills do you want to see?', 0, 20, 5)
# show_skills_and_words(skills_to_display, res_topics)
#
#
#
#     # top_skills = 4
#     # if top_skills > len(res_topics_ordered):
#     #     top_skills = len(res_topics_ordered)
#     # for i in range(top_skills):
#     #     skill = res_topics_ordered[i][0]
#     #     score = res_topics_ordered[i][1]
#     #     st.write('Skill #' + str(i+1) + ": " + str(skill) + ' score: ' + str(score))
#     #     st.write('Skill words: ' + str(topic_words[skill]))
#
# section_separator()
# """
# ## Jobs similar to this resume
# """
# similar_jobs_to_resume = st.slider('# similar jobs to selected resume', 0, 15, 5)
# predict_jobs(d2v_model, df, text=text_lookup_res, topn=similar_jobs_to_resume)
#
#
# section_separator()
# """
# ## Search for Jobs Similar to a Selected Job
# Pick a job number, see that job, you will be shown similar jobs
# """
# job_num = int(st.text_input(label="Enter a Job ID between 0 and 22000", value="-1"), 10)
# if job_num == -1:
#     st.warning('No job ID selected for search')
#     st.stop()
#
# similar_jobs_to_job = st.slider('# similar jobs to selected job', 0, 10, 5)
#
# st.write('#### Showing similar jobs to this one')
# print_job_info(job_num)
#
# # show similar jobs
# text_lookup_job = df.iloc[job_num]['job_description']
# predict_jobs(d2v_model, df, text=text_lookup_job, topn=similar_jobs_to_job)
#
#
# section_separator()
# """
# ## Here's the data behind this demo
# """
# short = df[:10000]
# st.write(short)
