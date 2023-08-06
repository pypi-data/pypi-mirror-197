import os

from SciAssist.utils.pdf2text import get_bodytext

from SciAssist.bin.doc2json.doc2json.grobid2json.process_pdf import process_pdf_file

root_dir = "/home/dingyx/project/SciAssist/data/pdfs/"
for dirpath,dirnames,files in os.walk(root_dir):
    file_list = files
    break
file_list.sort()
for i in file_list:

    filename=os.path.join(root_dir,i)

    json_file = process_pdf_file(input_file=filename)
    # Extract bodytext from pdf and save them in TEXT format.
    text_file = get_bodytext(json_file=json_file, output_dir="/home/dingyx/project/SciAssist/data/pdfs/")