import PyPDF2

from Assistant import synthesize_to_speaker

pdffileobj=open('Prajjawal_Agarwal_Resume.pdf','rb')
pdfreader = PyPDF2.PdfFileReader(pdffileobj)
x=pdfreader.numPages
page_obj = pdfreader.getPage(0)

synthesize_to_speaker(page_obj.extractText())
