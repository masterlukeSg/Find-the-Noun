import requests
from bs4 import BeautifulSoup
import re
from random import randint
from HanTa import HanoverTagger as ht



# TODO: Wörter, die eigentlich nichts mit dem Kontext zu tun haben, sollen nicht mitgezählt werden -> quelltext, literatur etc.

class Wiki:
    def __init__(self, rounds) -> None:
        self.soup = None
        self.rounds = rounds
        self.zweiterVersuch = None
        self.visited = []
        self.tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    def websiteFunctions(self, keywordForLink):
        link = keywordForLink
        url = f'https://de.wikipedia.org/wiki/{link}'
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        text = self.soup.get_text()
        return text
    
    def detectNoun(self, words):
        for word, x, pos in self.tagger.tag_sent([words], taglevel=1):
            if pos == 'NN':
                return True
        return False
        
        
    def main(self, keywordForLink):
        if self.rounds == 0 or keywordForLink == None:
            exit()
        self.rounds = self.rounds - 1 
        
        # Text von der HTML Seite 
        text = self.websiteFunctions(keywordForLink)
             
        #print(keywordForLink , " ", self.rounds)
       
        # alle Wörter einzeln in einer Liste
        wordlist = text.split()
        allWords = {}

        
        
        for word in wordlist:
            if (re.match(r'^[A-Z][a-z]*$', word)):
                
                if (self.detectNoun(word) == True):
                    
                    # wenn Wort schon vorkam -> counter erhöhen
                    if word in allWords:
                        allWords[word] =  allWords[word] + 1
                    else:
                        allWords[word] = 1
                    
        
        existingWords = {}
        
        # Wörter aus der "DB" auslesen
        with open('words.txt', 'r') as doc:
            for line in doc:
                wordWithValue = line.strip().split()
                if len(wordWithValue) == 2:
                    existingWords[wordWithValue[0]] = int(wordWithValue[1])
        
        # Werte erhöhren & Wort mit Wert neu hinzufügen
        for word, value in existingWords.items():
            if word in allWords:
                allWords[word] += value
            elif len(word) > 1 :
                allWords[word] = value
        
        # Wörter nach Wert sortieren
        allWords = dict(sorted(allWords.items(), key=lambda item: item[1], reverse=True))

        # "DB" bekommt wird wieder mit den Werten gefüllt
        with open('words.txt', 'w') as doc:
            for word, amount in allWords.items():
                doc.write(word + " " + str(amount) + "\n")
        
        # main wird erneut aufgerufen -> mit neuem Link
        keywordForLink = self.getNewLink()
        self.main(keywordForLink)
     
    def getNewLink(self):

        ### PART ONE: links die in Frage kommen extrahieren
        
        allLinks = [] 
        # strings die nicht im string sein sollen
        check_strings = ["http", "cite_ref", "cite_note", ".", ":", "%", "?", "searchInput", "-", "Weblinks", "#", "None"]

        # sucht alle mit a makierten html texte
        links = self.soup.find_all('a')
        for link in links:
                # nimmt nur strings, die als link gekennzeichnet werden 
                link = (str(link.get('href')))
                # link muss an erster stelle enthalten: wiki o. #
                # darf nicht enhalten: "siehe" check_strings 
                
                ## "wiki" or "#"
                if (("w" or "#" ==  link[0]) and all (sub not in link for sub in check_strings)):
                    
                    # link soll nur mit schlagwort in die Liste
                    if ("wiki" in link):
                        link = link.replace("/wiki/", "")
                    if ("#" in link):
                        link = link.replace("#" , "")
                    if link not in allLinks:
                        allLinks.append(link)


    
        for i in range(0, len(allLinks)):
            neuerLink = randint(0, len(allLinks)-1)

            if allLinks[neuerLink] not in self.visited and len(allLinks) > 0:
                self.visited.append(allLinks[neuerLink])
                
                # falls bei der nächsten Seite kein Link gefunden wird, wird von dieser Seite ein zweiter Link
                # als BackUp gespeichert. Dieser könnte dann nach der ForLoop zurückgegeben werden
                
                neuerIndex = randint(0, len(allLinks)-1)
                self.zweiterVersuch = allLinks[neuerIndex]
                return self.visited[-1]

        self.visited.append(self.zweiterVersuch)
        return self.zweiterVersuch
            
    
    
if __name__ == "__main__":
    w = Wiki(4025) 
    w.main("Deutschland")
    