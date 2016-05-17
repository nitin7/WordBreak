from wordsegment import clean, clean1
import sys
import os
import chardet
import unicodedata
import string
from stanford_corenlp_pywrapper import CoreNLP

MIN_PARA_SIZE = 4

def removeHeadings(article):
    data0 = article.read()
    data = data0
    try:
        code = chardet.detect(data)
        paragraphs = data.decode(code['encoding'], errors="ignore")
        data = unicodedata.normalize('NFKD', paragraphs).replace(u"\u2013", "-").encode('utf-8','ignore')
        data = str(unicode(data, errors='ignore'))
        splitData = data.split('\n')
        splitData = [para for para in splitData if para]
        splitData[0] = splitData[0].split('(')[0]
        title = ' '.join(splitData[0].split('_')).strip()
        i=0
        for i in range(1,len(splitData)):
            para = splitData[i]
            if len(para.split())<=MIN_PARA_SIZE:
                break
        finalParas = []
        for i in range(1,len(splitData)):
            para = splitData[i]
            if len(para.split())>MIN_PARA_SIZE:
                finalParas.append(para)
            else:
                if para in ['See also','Notes','References','External links']:
                    break
            data = '.'.join(finalParas)
        return data
    except:
        return data0

def main(arg):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
    configFileLoc = os.path.join(dir, 'config.ini')
    proc = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
    with open(arg, "r") as file:
        data = removeHeadings(file)
        parsed = proc.parse_doc(data)
        data = []
        for s in parsed[u'sentences']:
            sent = str(' '.join(s[u'tokens']))
            data.append(sent.translate(string.maketrans("",""), string.punctuation))

        data1 = ".".join(data)
        data1 = data1.replace("..",".")
        data1 = data1.replace("  "," ")
        data1 = data1.replace(" .",". ")
        data2 = " ".join(data)
        data2 = data2.replace("  "," ")
        file_train1 = open("data/a1_train1.txt", "w")
        file_train1.write(data1)
        file_train1.close()
        
        file_train2 = open("data/a1_train2.txt", "w")
        file_train2.write(data2)
        file_train2.close()
        
        file_test1 = open("data/a1_test1.txt", "w")
        file_test1.write(clean1(data1))
        file_test1.close()

        file_test2 = open("data/a1_test2.txt", "w")
        file_test2.write(clean(data2))
        file_test2.close()

if __name__ == '__main__':
    main(sys.argv[1])