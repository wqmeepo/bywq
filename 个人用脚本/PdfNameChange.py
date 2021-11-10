import os
import pdfplumber

file_path = 'D:/pdf/'
os.chdir(file_path)

for fileName in os.listdir():
    print('fileName=' + fileName)
    with pdfplumber.open(file_path + fileName) as pdf:
        words = pdf.pages[0].extract_words()[:3]
        pdfNewName = words[0]['text'] + words[1]['text'] + words[2]['text']

    print('new =' + pdfNewName)
    os.rename(fileName, pdfNewName + '.pdf')
