import os, sys, hashlib, hmac, ecdsa, codecs

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
    while not terminated:
        print("Que voulez vous faire ?")
        print("1) Générer une seed")
        print("2) Récupérer votre seed à partir d'une suite mnemonique")
        print("3) Récupérer votre Master Private Key et/ou votre Master ChainCode")
        print("4) Générer une Private Key à partir de son index et/ou de son niveau de dérivation") 
        print("5) Récupérer une Private Key à partir de son index et de son niveau de dérivation")

        input("Votre choix (chiffre) : ",end="")

#seed = generateSeed()
master = getMaster_privateKey_chainCode("5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570")
#print("BIP39 Mnemonic :",seed["Mnemonic"])
#print()
#print("BIP39 Seed :", seed["Seed"])
private_key = master["privateKey"]
print("private key :",private_key)
print("chain code :",master["chainCode"])
public_key = getPublicKeyFromPrivateKey(private_key)
print("public key :",public_key)
chainCode = master["chainCode"]
index = 0
child = getChild(master, "0/0")
publicChild = getPublicKeyFromPrivateKey(child["privateKey"])
print("public child :",publicChild)
print(len(bytearray.fromhex(publicChild)))
