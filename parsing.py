
#Note: Parsing time complexity is high.
import xml.etree.ElementTree as ET
import nltk
import csv
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

ps= PorterStemmer() # to steam each word
stopWords= list(set(stopwords.words("english"))) # list of common words
stopWords = [word for word in stopWords] # convering unicode string list to string list
femalePronounList=["her", "she", "herself", "hers", "her-self"]
malePronounList= ["he", "himself", "him", "his", "hims", "him-self"]


techList=[] # list of technology words
#reading technology words from file
try:
    fp_technical= open("technical_words.txt","r")
    techList=[word.decode('utf-8').strip('\n') for word in fp_technical.readlines()]
    fp_technical.close()
except:
    print "Can't open  technical_words file"


relationshipList=[]

#reading relationship  words from file
try:
    fp_relation= open("relationship_life.txt","r")
    relationshipList=[word.decode('utf-8').strip('\n') for word in  fp_relation.readlines()]
    fp_relation.close()
except:
    print "Can't open  relationship_life file"


# reading file names
files = []
genders = []
try:
    fp = open("truth.txt", "r")
    lines = fp.readlines()
    for i in lines:
        lineTokens = i.split(":::")

        files.append(lineTokens[0])
        genders.append(lineTokens[1])
    fp.close()
except:
    print "Can't open truth file"

# parsing each txt file
print "Count files in corpus"
def parsing(files):
    allTxtFiles=[]
    count=0
    for file in files:
        tree= ET.parse("en\\"+file+".xml")
        root= tree.getroot()
        txt=""
        for elem in root:
            for subelem in elem:
                txt+=subelem.text
        allTxtFiles.append(txt.lower().strip())
        count+=1
        print count
    return allTxtFiles





def checkExist(word, list):

    if  word != '' and word in list:
            return True
    return False




def iterateEachText(allAuthorFileLists, fileName):  # return detList

    with open(fileName, mode='wb' ) as f:
        try:
            fieldNames=['Determiner','Pronoun_Male','Pronoun_Female','Technical_Word','Relationship_And_Personal_Life','Preposition','Common_Word_Count','Gender' ]
            theWriter= csv.DictWriter(f,fieldnames=fieldNames)
            theWriter.writeheader()

            genderIndex = 0

            for text in allAuthorFileLists:
                gendr = 0 # 0 means female , 1 means male
                countDeterminer = 0
                countPronounMale = 0
                countPronounFemale = 0
                countTechnicalWord = 0
                countRelationAndLife = 0
                countPreposition = 0

                tokens = nltk.word_tokenize(text)
                commonWordList= list(set(tokens) & set(stopWords))
                countCommonlyUsedWords = len(commonWordList)

                if(len(tokens)!= 0):
                    part_of_speech = nltk.pos_tag(tokens)
                    print part_of_speech   # printing part_of_speech
                    for (word, tag) in part_of_speech:
                        if (tag == "DT"):
                            countDeterminer+=1
                        elif tag =="PDT":
                            countDeterminer+=1
                        elif tag=="WDT":
                            countDeterminer+=1
                        elif tag=="TO":   #preposition
                            countPreposition+=1
                        elif tag=="IN":     #preposition
                            countPreposition+=1
                        elif ((tag== "PRP" or tag=="PRP$") and (ps.stem(word) in femalePronounList)) : #pronoun female
                            countPronounFemale+=1
                        elif ((tag== "PRP" or tag=="PRP$") and (ps.stem(word) in malePronounList)): #pronoun male
                            countPronounMale+=1
                        elif (checkExist(ps.stem(word), techList)):
                            countTechnicalWord+=1
                        elif (checkExist(ps.stem(word),relationshipList)):
                            countRelationAndLife+=1
                if (genders[genderIndex]=="male"): # genders in my global list
                      gendr=1
                genderIndex += 1
                 #writing to CSV file
                theWriter.writerow({'Determiner': countDeterminer,'Pronoun_Male':countPronounMale ,'Pronoun_Female': countPronounFemale, 'Technical_Word':countTechnicalWord,'Relationship_And_Personal_Life':countRelationAndLife,'Preposition':countPreposition,'Common_Word_Count':countCommonlyUsedWords,"Gender":gendr })

            f.close()
        except:
            print "IO error"





authorTextLists = parsing(files)  # passing file names #return list for all Author's Txt

iterateEachText(authorTextLists,"gender.csv") # iterate through file and write dictionary values to csv file
