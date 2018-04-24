import nltk
import os
import re
import io


txtDir = 'C:\\Users\\Lenovo\\Documents\\files\\'
metaPath = 'C:\\Users\\Lenovo\\Documents\\'

#megnyitja a fajlokat, ami benne van a parseolt txtDir-ben
def referencesFind(txtDir, metaPath):
        for txt in os.listdir(txtDir):
                textFile = open(txtDir + txt, "r", encoding='utf-8')
                text = textFile.read()
                sents = nltk.sent_tokenize(text)
                references = re.compile(r'\(\'(\d+)\'\,\s\'(.*?\"|.*?\:)(.*?\"|.*?\.)(.*?\')\)', re.MULTILINE)
                line_list = []
                number_list = []
                author_list = []
                publication_list = []
                otherInfo_list = []
                ref_list = []

# megkeresi a hivatkozasokat a parseolt txt-ben (4 capturing group + full match)

                for line in references.finditer(text):
                        number, author, publication, otherInfo = line.groups()      # itt vannak a capturing groupok
                        number_list.append(number)                                  # a hivatkozasszam, ami alapjan majd keresunk a txt-ben
                        for number in number_list:                                  # [1] ilyen formatumba keresse
                                number = number.replace(number, "["+number+"]")
                        author_list.append(author)                                  # szerzo(k)
                        publication_list.append(publication)                        # publikacios cim
                        for publication in publication_list:                                             # ideiglenes megoldas, most meg a fejlok neve a publication
                                remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
                                publication = publication.translate(remove_punctuation_map)              # kesobb az adott faj ID-ja lesz
                        otherInfo_list.append(otherInfo)                            # minden mas (miben, hol publikaltak, stb.)
                        ref_list.append(line)

# keresi a szovegben a cross reference-eket a felismert szamok alapjan es kiirja fajlba (jelenleg cikk came + txt)

                        for count, line in enumerate(sents):
                                        line_list.append(line)
                                        if number in line and "]" not in line_list[count-1]:    # ha van az elozo mondatban '[' (tehat masik hivatkozas) ne irja ki
                                                filename = metaPath + publication + ".txt"
                                                f = open(filename, "ab+")                       # ha letezik append, ha nem akkor kreal egy ilyen fajlt
                                                f.write(line.encode("utf-8"))
                                                f.close()
                textFile.close()
