import nltk
import os
import re
import io
import json
from copy import copy, deepcopy

def referencesFind(txtDir, metaPath):

        refs = {}               #python dict, amiben az egymashoz tartozo elemek vannak (id - hivatkozas - szoveg)
        for txt in os.listdir(txtDir):
                textFile = open(txtDir + txt, "r", encoding='utf-8')
                name = textFile.name
                text = textFile.read()
                text2 = deepcopy(text)
                text = replaceNumbers(text2)
                sents = nltk.sent_tokenize(text)
                replaceNumbers(text)
                references = re.compile(r'(\(\'(\d+)\'\,\s\'(.*?)\'\))', re.MULTILINE)            #egyszerusitettem a regexet, hogy felismerje a egyseges formara hozott referenciakat
                line_list = []                                                                  
                number_list = []
                publication_list = []
                ref_list = []
                
                if name not in refs:
                        refs[name] = {}
                                                
                for line in references.finditer(text):
                        refz, number, publication = line.groups()
                        number_list.append(number)
                        publication_list.append(publication)
                        #for publication in publication_list:                                   #ha esetlegesen el kene tuntetni a specialis karaktereket, benne hagytam
                                #remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
                                #publication = publication.translate(remove_punctuation_map)
                        for number in number_list:
                                number1 = number.replace(number, "["+number)
                                number2 = number.replace(number, number+"]")
                        ref_list.append(refz)

                        if publication not in refs[name]:
                                refs[name][publication] = []
                                
                        for count, line in enumerate(sents):
                                line_list.append(line)
                                lineBefore = 0
                
                                if (number1 or number2) in line:
                                        if "]" not in line_list[count-1]:
                                                if line_list[count-1] not in ref_list:
                                                        lineBefore = line_list[count] + line_list[count-1]
                                        else:
                                                lineBefore = line_list[count]
                                        if lineBefore not in refs[name][publication]:
                                                refs[name][publication].append(lineBefore)
                                        
                
        textFile.close()

        with open('references.json', 'w+') as outfile:
                json.dump(refs, outfile, indent =4)                     #pretty printingeljuk a dictunket 


txtDir = 'C:\\Users\\Lenovo\\Documents\\files\\'
metaPath = 'C:\\Users\\Lenovo\\Documents\\'

referencesFind(txtDir, metaPath)
