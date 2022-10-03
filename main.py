import os, sys, hashlib, hmac, ecdsa, codecs
from bip32 import BIP32

def generateEntropy():
    rng = os.urandom(16)
    h = hashlib.sha256()
    h.update(rng)
    rng = ''.join(bin(int(x))[2:].zfill(8) for x in rng)
    hashe = ''.join(bin(int(x))[2:].zfill(8) for x in h.digest())
    return rng + hashe[:4]

def convertMnemonicToBinary(mnemonic):
    words = [word[:-1] for word in open("english.txt")] #Importing the mnemonic english dictionnary (provided by BTC github)
    wordMapping = [words.index(w) for w in mnemonic.split()] #Getting corresponding number of each word in the dictionnary
    fullSeed = ''.join(bin(w)[2:].zfill(11) for w in wordMapping) #Converting each number to a 11-bits sized binary number and joining them

    return fullSeed

def convertBinaryToMnemonic(binary):
    slices = [binary[i:i+11] for i in range(0,len(binary),11)] #Slicing the seed in 11-bits sized slices (total of 12 slices)

    words = [word[:-1] for word in open("english.txt")] #Importing the mnemonic english dictionnary (provided by BTC github)

    mnemonic = ' '.join(words[int(m,2)] for m in slices) #Getting the corresponding mnemonic word to each slice of the previously sliced seed

    return mnemonic

def generateSeed():
    rngSeed = generateEntropy()

    mnemonic = convertBinaryToMnemonic(rngSeed)

    h = hashlib.pbkdf2_hmac( "sha512", mnemonic.encode("UTF-8"), "mnemonic".encode("UTF-8"), 2048)
    seed = ''.join(bin(int(x))[2:].zfill(8) for x in h)

    return { "Mnemonic" : mnemonic, "Binary" : rngSeed, "Seed" : hex(int(seed,2))[2:] }

def getSeedFromMnemonic(mnemonic):
    rngSeed = convertMnemonicToBinary(mnemonic)
    h = hashlib.pbkdf2_hmac( "sha512", mnemonic.encode("UTF-8"), "mnemonic".encode("UTF-8"), 2048)
    seed = ''.join(bin(int(x))[2:].zfill(8) for x in h)
    return { "Mnemonic" : mnemonic, "Binary" : rngSeed, "Seed" : hex(int(seed,2))[2:] }

def getMaster_privateKey_chainCode(seed):
    byteArraySeed = bytearray.fromhex(seed)
    keyWord = "Bitcoin seed".encode("UTF-8")
    h = hmac.new(key = keyWord, msg = byteArraySeed, digestmod = hashlib.sha512)
    result = h.digest()
    return {"privateKey" : result[:32].hex(),"chainCode" : result[32:].hex()}

def getPublicKeyFromPrivateKey(private_key):
    byte_array = bytearray.fromhex(private_key)
    public_key_raw = ecdsa.SigningKey.from_string(byte_array,curve=ecdsa.SECP256k1).verifying_key

    public_key_hex = codecs.encode(public_key_raw.to_string(), 'hex')
    public_key_uncompressed = (b'04' + public_key_hex).decode("utf-8")

    if (ord(bytearray.fromhex(public_key_uncompressed[-2:])) % 2 != 0):
        public_key_compressed = '03'
    else:
        public_key_compressed = '02'

    public_key_compressed += public_key_uncompressed[2:66]
    return public_key_compressed

def getChild(parent, index):
    current = parent
    indexes = [int(x).to_bytes(4,"big") for x in index.split('/')]
    for i in indexes:
        currentKey = bytearray.fromhex(getPublicKeyFromPrivateKey(current["privateKey"]))
        currentChainCode = bytearray.fromhex(current["chainCode"])
        h = hmac.new(key = currentChainCode, msg = currentKey + i, digestmod = hashlib.sha512)
        result = h.digest()
        current = {"privateKey" : result[32:].hex(), "chainCode" : result[:32].hex()}
    return current

def menu(): 
    terminated = False
    seed = None
    while not terminated:
        print("Que voulez vous faire ?")
        print("1) Générer une seed")
        print("2) Saisir une seed (hexadécimale)")
        print("3) Récupérer votre seed à partir d'une suite mnemonique")
        print("4) Extraire votre Master Private Key, votre Master ChainCode ainsi que votre Master Public Key")
        print("5) Générer une clé enfant à partir de son index et de son niveau de dérivation") 

        x = input("Votre choix (chiffre) : ")
        try:
            ans = int(x)
        except:
            input("Mauvaise entrée : veuillez saisir le numéro de l'action de votre choix ( Pressez entrer pour continuer )")
            os.system("cls")
            continue
        if ans > 5 or ans < 1:
            input("Le chiffre entré est incorrect, veuillez saisir un chiffre correspondant à une action affichée ( Pressez entrer pour continuer )")
            os.system("cls")
            continue
        if ans == 1:
            seed = generateSeed()
            print("Voici votre seed en hexadécimal :",seed["Seed"])
            print("Voici votre suite mnemonique (correspondant à la seed ci-dessus) :",seed["Mnemonic"])
            print("Vous avez désormais une seed active utilisable pour les prochaines actions !")
        if ans == 2:
            seed = input("Veuillez saisir votre seed en hexadécimal : ")
            try:
                int(seed,16)
            except:
                print("Seed incorrect (hexadécimal obligatioire ou choisissez le choix n°3 pour importer une suite mnémonique)")
        if ans == 3:
            m = input("Veuillez saisir votre suite mnemonique : ")
            while len(m.split()) != 12:
                print("Votre suite mnemonique doit être composée de 12 mots")
                m = input("Veuillez la saisir à nouveau : ")
            try:
                seed = getSeedFromMnemonic(m)
            except:
                seed = None

            while seed == None:
                print("Seed incorrect")
                m = input("Veuillez la saisir à nouveau : ")
                try:
                    seed = getSeedFromMnemonic(m)
                except:
                    seed = None
            print("Vous avez désormais une seed active utilisable pour les prochaines actions !")
        if ans == 4:
            if seed != None:
                ans = input("Souhaitez vous utiliser la seed active ? (Y/n) : ").lower()
                while ans != "y" and ans != "n":
                    ans = input("Veuillez saisir Y ou n (non sensible à la case) : ").lower()
                if ans == "n" :
                    input("Veuillez sélectionner l'action 1 ou 2 pour obtenir une seed active dans le menu ( Pressez entrer pour continuer )")
                    continue
            else:
                input("Veuillez sélectionner l'action 1 ou 2 pour obtenir une seed active dans le menu ( Pressez entrer pour continuer )")
                continue
            master = getMaster_privateKey_chainCode(seed["Seed"])
            print("Votre Master Private Key (hexadécimal) :", master["privateKey"])
            print("Votre Master Chain Code (hexadécimal) :", master["chainCode"])
            print("Votre Master Public Key (hexadécimal) :", getPublicKeyFromPrivateKey(master["privateKey"]))
        if ans == 5:
            if seed != None:
                ans = input("Souhaitez vous utiliser la seed active ? (Y/n) : ").lower()
                while ans != "y" and ans != "n":
                    ans = input("Veuillez saisir Y ou n (non sensible à la case) : ").lower()
                if ans == "n" :
                    input("Veuillez sélectionner l'action 1 ou 2 pour obtenir une seed active dans le menu ( Pressez entrer pour continuer )")
                    continue
            else:
                input("Veuillez sélectionner l'action 1 ou 2 pour obtenir une seed active dans le menu ( Pressez entrer pour continuer )")
                continue
            print("Le format pour choisir un niveau de dérivation avec les index de chaque dérivation est : m/index1/index2/index3...")
            path = "m/"+input("Veuillez saisir le chemin de dérivation désiré : m/")
            b = BIP32.from_seed(bytearray.fromhex(seed["Seed"]))
            child = b.get_pubkey_from_path(path).hex()
            print(f"La clé publique de l'enfant de chemin {path} est (hexa) : {child}")
        a = input("DONE ( Veuillez presser entrer pour continuer 'q' pour quitter ) ")
        terminated = a.lower() == 'q'
        os.system("cls")


menu()
            




