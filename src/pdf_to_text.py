
import os, sys
import numpy as np
import pdfplumber



def main():
    # load image
    if len(sys.argv) < 4:
        sys.exit('pdf_to_text.py [pdf_file] [save_name] [binary true/false] ...')
        pass
    else:
        # './' if running oer_demo, else '../' for command line
        PDF_PATH = './data/pdf/'
        TXT_PATH = './data/text/'
        pdf_filename= str(sys.argv[1])
        save_name = str(sys.argv[2])
        bin = str(sys.argv[3]).lower()
        pdf_name = pdf_filename[0:pdf_filename.index('.')]
        pdf_ext = pdf_filename[pdf_filename.index('.'):]
        print('reading: ' + pdf_filename)
        print('from: ' + PDF_PATH)
        print('saving as: ' + save_name + '.txt')
        if bin == 'true':
            with open(PDF_PATH + pdf_filename, 'rb') as f:
                pdf = pdfplumber.open(f)
                print('loaded binary pdf')
                with open(TXT_PATH + save_name + '.txt', 'a') as output:
                    for i in range(len(pdf.pages)):
                        output.write(pdf.pages[i].extract_text())
                        output.write('\n' + '===== END page {} ====='.format(i+1) + '\n')
        else:
            pdf = pdfplumber.open(PDF_PATH + pdf_filename)
            print('loaed regular pdf')
            with open(TXT_PATH + save_name + '.txt', 'a') as output:
                for i in range(len(pdf.pages)):
                    output.write(pdf.pages[i].extract_text())
                    output.write('\n' + '===== END page {} ====='.format(i+1) + '\n')

        print('\nwrote to ' + TXT_PATH + save_name + '.txt')



if __name__ == "__main__" :
    main()
