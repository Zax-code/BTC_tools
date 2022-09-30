import os, sys, hashlib, hmac

def generateEntropy():
    rng = os.urandom(16)
    h = hashlib.sha256()
    h.update(rng)
    rng = ''.join(bin(int(x))[2:].zfill(8) for x in rng)
    hashe = ''.join(bin(int(x))[2:].zfill(8) for x in h.digest())
    return rng,hashe

def generateSeed():
    rng, hashe = generateEntropy() #Generate entropy with its sha256 hash
    fullSeed = rng + hashe[:4] #Adding checksum (last 4 bits of hash) to the entropy

    slices = [fullSeed[i:i+11] for i in range(0,len(fullSeed),11)] #Slicing the seed in 11-bits sized slices (total of 12 slices)

    words = [word[:-1] for word in open("english.txt")] #Importing the mnemonic english dictionnary (provided by BTC github)
    mnemonic = ' '.join(words[int(m,2)] for m in slices) #Getting the corresponding mnemonic word to each slice of the previously sliced seed

    return mnemonic

def convertMnemonicToBinary(mnemonic):
    words = [word[:-1] for word in open("english.txt")] #Importing the mnemonic english dictionnary (provided by BTC github)
    wordMapping = [words.index(w) for w in mnemonic.split()] #Getting corresponding number of each word in the dictionnary
    fullSeed = ''.join(bin(w)[2:].zfill(11) for w in wordMapping) #Converting each number to a 11-bits sized binary number and joining them

    return fullSeed[:-4]

def getMaster_PK_ChainCode(seed):

    byteSeed = bytes([int(seed[i:i+8],2) for i in range(0,len(seed),8)])
    h = hashlib.sha512()
    h.update(byteSeed)
    hashBit = ''.join(bin(int(i))[2:].zfill(8) for i in h.digest())

    return {"Master Private Key" : hashBit[:256],"Master Chain Code" : hashBit[256:]}

def menu(): 
    terminated = False
    while not terminated:
        print("Que voulez vous faire ?")
        print("1) Créer une seed")

        input("Votre choix (chiffre) : ",end="")

print(getMaster_PK_ChainCode(convertMnemonicToBinary(generateSeed())))
