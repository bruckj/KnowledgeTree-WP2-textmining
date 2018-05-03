import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import nltk 
import re
import json
from collections import defaultdict


class SectionParser:
    def __init__(self, document, sections):
        self.document = document
        self.sections = sections
    
    def parse_sections(self):
        """végigiterál a dokumentumon és felbontja a szöveget
        a fejezetcímek szerint fejezetekre"""
        
        # olyan, mint egy sima dict, csak nem létező kulcsra
        # üres stringet ad KeyError dobálás helyett
        section_mapping = defaultdict(str)
        section = None

        for line in self.document.split('\n'):
            if self.line_is_section_header(line):
                section = line
                
            elif section:
                section_mapping[section] += line
        return section_mapping

    def line_is_section_header(self, line):
        """megvizsgálja, hogy a sor  fejezetcím-e"""
        
        if line in self.sections:
            return line

def convert(fname, pages=None):
     """maga a konvertálás ebben a függvényben történik meg, visszatérési értéke
    a szöveg tartalma stringként"""
        
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

def convertJSONMultiple(pdfDir, JSONDir):
     """átkonvertálja az összes pdfet, ami a pdfDir mappában található és menti 
    .json fájlként őket a JSONDir mappába"""
    if pdfDir == "": pdfDir = os.getcwd() + "\\" 
    for pdf in os.listdir(pdfDir): #végigiterál az összes pdf-en a mappában
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf 
            text = convert(pdfFilename) #megkapja stringként a pdf szövegét
              #ahhoz, hogy az Abstract is egy kulcs legyen külön sorban kell szerepelnie 
            textR = text.replace('Abstract','\nAbstract\n') 
            if 'Abstract' not in textR:
                textR = text.replace('ABSTRACT','\nAbstract\n')
            
            references = textR.find('REFERENCES')
            if 'REFERENCES' not in textR:
                references = textR.find('References')
            text = textR[:references]
            
            #ahhoz, hogy egy hivatkozás egy objektum legyen regexet használ
            refList = textR[references:].replace('\n','')
            ref = nltk.regexp_tokenize(refList, r'\[(\w+)\]([^\[]+)')
            refstr = ''.join(str(r) for r in ref)
            
            document = text + 'REFERENCES' + '\n' +refstr
            
            titleAuthors = textR.find('Abstract')
            titleAuthorsStr = text[:titleAuthors].replace('\n',' ')
            
            #a fejezetcímek az alábbi 3 regexre illeszkednek:
            #1.: arab szám, nulla vagy egy pont, szóköz és utána vagy végig nagy betű
            #vagy csak az első karakter nagy betű
            #2.: római szám,nulla vagy egy pont, szóköz és utána vagy végig nagy betű
            #vagy csak az első karakter nagy betű
            #3.: egy darab nagybetű, egy darab pont, szókö és utána vagy végig nagy betű
            #vagy csak az első karakter nagy betű
            titleRE_list = [r'\n([0-9]\.?\s[A-Z][a-zA-Z0-9].+)\n', 
                          r'\n\n([I|V|X]{1,4}\.?\s[a-zA-Z0-9].+)\n', 
                          r'\n[A-Z]{1}\.\s[A-Z][a-zA-Z0-9].+\n']
            
            #a címeket egy listában tároljuk el, ezt adjuk át a 
            #SectionParser osztályban szereplő függvényeknek 
            sectiontitles = list()
            for regex in titleRE_list:
                sectiontitles += re.findall(regex, text) 
               #for regexToSub in titleRE_list:
                   #sectiontitles += re.findall(regexToSub, text)
            
            sectiontitles.insert(0, 'Abstract')
            sectiontitles.insert(1, 'INTRODUCTION')
            sectiontitles.append('References')
            sectiontitles.append('REFERENCES')
            
            sp = SectionParser(document, sectiontitles)
            sec = sp.parse_sections()
        
            #dictionary készítése a címek a kulcsok, 
            #a hozzájuk tartozó érték pedig szövegrészletek
            dictionary = {'Title and Authors': titleAuthorsStr}            
            dictionary.update(sec) 
           
            #a .json fájl előállítása
            JSONFilename = JSONDir + pdf.split('.')[0]  + ".json"            
            #a címből kiszedi az idt, ez lesz egy külső dictionarynek
            #a kulcsa értéke pedig maga a szöveg
            id1 = pdf.split('.pdf')[0]
            id = id1.split('/')[-1]
            dictWithId = {id : dictionary}
            #fájl megnyitása írásra, majd maga az írás is megtörténik 
            JSONFile = open(JSONFilename, "w", encoding='utf-8') 
            json.dump(dictWithId, JSONFile, ensure_ascii=False, indent=4)
                 
pdfDir = "/mnt/datasharepoint-pdf/openacademic/"
JSONDir= "/mnt/datasharepoint-txt/"
convertJSONMultiple(pdfDir, JSONDir)
