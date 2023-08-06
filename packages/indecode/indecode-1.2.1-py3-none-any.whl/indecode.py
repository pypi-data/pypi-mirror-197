import random
__version__="1.2.1"
text="hello"
carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
def generate_key():
    carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
    random.shuffle(carac)
    key=""
    for i in range(len(carac)):
        key=key+carac[i]
    return key
def code(text,key):
    newtext=""
    incode={}
    liste=[]
    for i in range(len(key)):
        incode.update({carac[i]:key[i]})
    incode.update({" ":" "})
    for i in range(len(text)):
        newtext=newtext+incode[text[i]]
    return newtext
def decode(test,key):
    newtext=""
    uncode={}
    for i in range(len(key)):
        uncode.update({key[i]:carac[i]})
    uncode.update({" ":" "})
    for i in range(len(test)):
        newtext=newtext+uncode[test[i]]
    return newtext
if __name__=="__main__":
    keya=generate_key()
    print(keya)
    icode=code(text,keya)
    print(icode)
    decod=decode(icode,keya)
    print(decod)