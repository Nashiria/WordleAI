from nltk.corpus import words
import random
word_list = [x.lower() for x in words.words() if len(x)==5]
alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def frequencyList():
    letterDict={}
    for word in word_list:
        for letter in word:
            letter=letter.lower()
            if letter in letterDict:
                letterDict[letter] += 1
            else:
                letterDict[letter] = 1
    for letter in alphabet:
        print(letter.capitalize(),",",letterDict[letter])
def powerList():
    letterDict={}
    powerList=[]
    for word in word_list:
        for letter in word:
            letter=letter.lower()
            if letter in letterDict:
                letterDict[letter] += 1
            else:
                letterDict[letter] = 1
    for word in word_list:
        power=0
        if len(list(dict.fromkeys(word)))==len(word):
            for letter in word:
                power+=letterDict[letter]
            powerList.append([word,power])
    powerList.sort(key = lambda x: x[1],reverse=True)
    return powerList
def randomWord(wordlist):
    randomWord=random.choice(wordlist)
    return randomWord
def result(word,guess):
    result=[]
    for index in range(len(guess)):
        if guess[index]==word[index]:
            result.append("G")
        elif guess[index] in word:
            result.append("Y")
        else:
            result.append("N")
    return result
def modifyKnowledge(chosen,guess,knowledge):
    if knowledge=={}:
        knowledge["letters"]={}
        knowledge["must"]=[]
        for _ in range(len(guess)):
                knowledge["letters"][_]=alphabet.copy()            
    results=result(chosen,guess)
    for index in range(len(results)):
        if results[index]=="G":
            knowledge["letters"][index]=[guess[index]]
            if guess[index] not in knowledge["must"]:
                knowledge["must"].append(guess[index])
        elif results[index]=="Y":
            knowledge["letters"][index].remove(guess[index])
            if guess[index] not in knowledge["must"]:
                knowledge["must"].append(guess[index])
        elif results[index]=="N":
            for _ in range(len(guess)):
                if guess[index] in knowledge["letters"][_]:
                    knowledge["letters"][_].remove(guess[index])
    return knowledge,results

def modifyRemaining(chosen,guess,knowledge):
    remaining=[]
    
    knowledge,results=modifyKnowledge(chosen,guess,knowledge)
    for word in word_list:
        possible=True
        for index in range(len(word)):
            letter=word[index]
            if letter not in knowledge["letters"][index]:
                possible=False
        for letter in knowledge["must"]:
            if letter not in word:
                possible=False
        if possible:
            remaining.append(word)
    return remaining,knowledge,results


def play():
        guess=input("First guess: ")
        word=input("Word we're looking for (r for random): ")
        if word=="r":
            word=randomWord(word_list)
        results=[]
        tries=1
        triedWords=[]
        knowledge={}
        working=True
        while working:
                    guesslist,knowledge,results = modifyRemaining(word,guess,knowledge)
                    print(guess,":",results)
                    if(results==["G","G","G","G","G"]):
                        working=False
                    else:
                        guess=randomWord(guesslist)
                        while guess in triedWords:
                            guesslist.remove(guess)
                            guess=randomWord(guesslist)
                        triedWords.append(guess)
                        tries+=1
        print("It took "+str(tries)+" tries to find '"+word+"'.\n")
play()
