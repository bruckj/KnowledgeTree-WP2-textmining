#a paraméterként kapott mappában lévő txtket strukturált formára hozza, a hivatkozásokig egy token egy mondat, 
#a hivatkozásoktól pedig egy hivatkozás egy token, végül felülírja a szöveges fájlok tartalmát ezzel a formátummal
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
