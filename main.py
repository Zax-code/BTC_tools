import os, sys, hashlib

def generateEntropy():
    rng = os.urandom(16)
    h = hashlib.sha256()
    h.update(rng)
    rng = ''.join(bin(int(x))[2:].zfill(8) for x in rng)
    hashe = ''.join(bin(int(x))[2:].zfill(8) for x in h.digest())
    return rng,hashe

def generateSeed():
    rng, hashe = generateEntropy()
    result = rng + hashe[:4]
    print(result)
    print("taille : ",len(result))
    slices = [result[i:i+11] for i in range(0,len(result),11)]
    print("morceaux : ",slices)
    words = [word[:-1] for word in open("english.txt")]
    mnemonic = ' '.join(words[int(m,2)] for m in slices)
    print(mnemonic)

def menu(): 
    terminated = False
    while not terminated:
        print("Que voulez vous faire ?")
        print("1) Créer une seed")

        input("Votre choix (chiffre) : ",end="")

generateSeed()    
