'''
Natural Language Processing of PDF documents
'''
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
mypdf = open('/home/timothy/NLP/test_doc.pdf', mode='rb')
pdf_document = PyPDF2.PdfFileReader(mypdf)
print(pdf_document.numPages)

number_of_pages = pdf_document.getNumPages()
text = 'begin: '
for i in range(number_of_pages):
    page = pdf_document.getPage(i)
    page_content = page.extractText()
    text = text+page_content
    
senteces = sent_tokenize(text)
words = word_tokenize(text)