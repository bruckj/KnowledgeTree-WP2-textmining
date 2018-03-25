import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import nltk 
import tempfile

#maga a konvertálás ebben a függvényben történik meg, visszatérési értéke a szöveg tartalma stringként
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()

    output.close
    return text 

#átkonvertálja az összes pdfet, ami a pdfDir mappában található és menti txt fájlként őket a txtDir mappába
def convertMultiple(pdfDir, txtDir):
    if pdfDir == "": pdfDir = os.getcwd() + "\\" 
    for pdf in os.listdir(pdfDir): #végigiterál az összes pdf-en a mappában
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf 
            text = convert(pdfFilename) #megkapja stringként a pdf szövegét
            textFilename = txtDir + pdf + ".txt"
            textFile = open(textFilename, "w", encoding='utf-8') #text fájl készítése
            textFile.write(text) #a pdfből kinyert tartalom text fájlba írása
           
#az előállított txt fájlok tokenizálása mondatokra, a hivatkozások tokenizálása pedig regexel történik,
#struktúrált formátum előállítása, majd a txt fájlok felülírása ezzel a formátummal 
def tokenizeText(txtDir):
    for txt in os.listdir(txtDir):
        tmp = tempfile.NamedTemporaryFile(mode="r+", encoding='utf-8')
        textFile = open(txtDir + txt, "r", encoding='utf-8')
        textR = textFile.read()
        references = textR.find('REFERENCES')
        
        text = nltk.sent_tokenize(textR[:references].replace('\n',''))
        ttstr = ''.join(text)
        tmp.write(ttstr.rstrip()+"\n")
        
        refList = textR[references:].replace('\n','')
        ref = nltk.regexp_tokenize(refList, r'\[(\d+)\]([^\[\]]+)')
        refstr = ''.join(str(r) for r in ref)
        tmp.write(refstr.rstrip()+"\n")
        
        textFile.close() #input fájl bezárása, hiszen csak olvasásra volt megnyitva
        tmp.seek(0) #átmeneti fájl értesítése
        o = open(txtDir + txt, "w", encoding='utf-8') #a text fájl megnyitása írásra

        #az eredeti fájl felülírása az idegigelens fájl tartalmával          
        for line in tmp:
            o.write(line)  

        tmp.close()   

pdfDir = "C:/Users/Sylvi/Desktop/Suli/Onlab/pdf/"
txtDir = "C:/Users/Sylvi/Desktop/Suli/Onlab/txt/"

convertMultiple(pdfDir, txtDir)           
tokenizeText(txtDir)            
