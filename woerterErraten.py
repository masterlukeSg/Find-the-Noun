


def defineConstrains(descriptionText, vorhandeneConstrains, pos = None, stoppKeyword = "fertig"):
    constrainsList, positionList= [], []
    position = None
    ersteConstrain = None
    
    print("\n-------------------------------------------------------------------")
    print("Schreibe '" + stoppKeyword + "' um die Abfrage zu beenden")
    print(descriptionText)
    
    while(True):
        
        if (len(vorhandeneConstrains) > 0): 
            print("Vorhandene Buchstaben: " , vorhandeneConstrains)
        
        ersteConstrain = input("Neue Buchstaben eingeben: ")
        #print("\n")
        
        if (ersteConstrain == stoppKeyword):
            return constrainsList, positionList
        
        if (pos == 1):
            while (True):
                try:
                    position = int(input("An welcher Stelle [1, 2,....]: "))
                except Exception:
                    print("Bitte gib nur Zahlen ein!")
                    position = int(input("An welcher Stelle [1, 2,....]: "))
                else: 
                    break        
                
            if (position not in positionList and len(ersteConstrain) == 1):
                constrainsList.append(ersteConstrain.upper())
                positionList.append(position - 1 )
        
        elif (pos == None and len(ersteConstrain) == 1):
                constrainsList.append(ersteConstrain.upper())
        
    

def checkInWordForConstrains(listOfWords, notInWord, inWordWrong, inWordWrongPOS, inWordRight, inWordRightPOS ):
    # notInWord -> Gar nicht im Wort enthalten
    
    #inWordWrong -> Im Wort enthalten, aber an der falschen Stelle
        #inWordWrongPOS -> Position von dem Buchstaben
    
    #inWordRight -> Im Wort enthalten und an der richtigen Stelle
        #inWordRightPOS -> Position vom Buchstaben
    
    
    legalWords = []
   
    for word in listOfWords:
        check = True
        
        if (len(notInWord) > 0):
            for notIn in notInWord:
                if notIn.upper() in word:
                    check = False

                
        if inWordWrong and inWordWrongPOS:
            for wrong, pos in zip(inWordWrong, inWordWrongPOS):
                if word[pos] == wrong:
                    check = False
                

        if inWordRight and inWordRightPOS:
            for right, pos in zip(inWordRight, inWordRightPOS):
                if len(word) > pos and word[pos] != right:
                    check = False


        for letter in inWordWrong:
            if (letter not in word):
                check = False
            
        if (check == True):
            legalWords.append(word)
    
    return legalWords
    
    
def main():
    lenOfWord = int(input("Wie lang ist das Wort?: "))
        
    orgList = []
    with open('words.txt', 'r') as doc:
        for wordsAndValue in doc:
            listOfWordsAndValue = wordsAndValue.strip().split()
            word = listOfWordsAndValue[0].upper()
            if (len(word) == lenOfWord):
                orgList.append(word)


        
    notInword, posNotInWord = [], []
    inWordRightPos, posRightInWord = [], []
    inWordWrongPos, posWrongInWord = [], []

    
    validWords = orgList    
    for i in range (0,5):
        
        notInword, posNotInWord = defineConstrains("Welche Buchstaben kommen im Wort gar nicht vor ?", notInword)

        inWordWrongPos, posWrongInWord = defineConstrains("Welche Buchstaben kommen vor, aber an der falschen Stelle ?", inWordWrongPos, pos=1)
    
        inWordRightPos, posRightInWord = defineConstrains("Welche Buchstaben kommen an der richtigen Stelle vor ?", inWordRightPos, pos=1)


        validWords = checkInWordForConstrains(validWords, notInword, inWordWrongPos, posWrongInWord,inWordRightPos, posRightInWord)
        print(validWords)
        if (len(validWords) > 0):   
            print(validWords[1])
        else:
            print("Leider konnte das Wort nicht gefunden werden.")


if __name__ == "__main__":
    main()