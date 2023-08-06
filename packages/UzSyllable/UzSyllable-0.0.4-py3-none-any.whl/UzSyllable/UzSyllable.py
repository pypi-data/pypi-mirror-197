def syllables(text):
    tokens=__preprocess(text)
    sylls=list()
    for token in tokens:
        count = 0
        vowels=set("AaEeUuOoIi")
        syll = list()
        start = 0
        for letter in token:
            for i in range(65,91):            
                if ord(letter) == i:
                    count += 1
        if count>1:
            sylls.append(token) 
            continue 
        count=0        
        for letter in token:
            if letter in vowels:
                count += 1
        if count == 1:
            sylls.append(token) 
            continue  

        for i in range(2, len(token)):
            if token[i] in vowels and token[i - 1] not in vowels: 
                w = token[start: i - 1]
                if len(w) != 0:
                    syll.append(w)
                    start = i - 1
            if token[i] in vowels and token[i - 1] in vowels:
                w = token[start: i]
                if len(w) != 0:
                    syll.append(w)
                    start = i
        w=token[start:len(token)]
        syll.append(w)
        count=0
        for i in syll[0]:
            if i in vowels: count+=1
        if count==0 :
            s=syll[1]
            syll[1]=syll[0]+s
            syll[0]=""
        if count==1:
            for i in range(1,len(syll)):            
                if syll[i][0] == 'h' or syll[i][0] =="'":
                    if syll[i-1][len(syll[i-1])-1] in ['s','c'] or syll[i][0]== "'":
                        s=syll[i]
                        syll[i] = syll[i-1][len(syll[i-1])-1] + s
                        s=syll[i-1]
                        syll[i-1]=s[0:len(s)-1]
            str=""
            for w in syll:
                if w != '': str+=w+'-'
            sylls.append(str[0:len(str)-1])
    return sylls

def __preprocess(text):
    return text.split()

def line_break(token):
    count = 0
    u=set("AaEeUuOoIi")
    txt = list()
    for h in token:
        if h in u:
            count += 1
    if count == 1 or len(token) < 4:
        return token
    count=0 
    for letter in token:
        for i in range(65,91):            
            if ord(letter) == i:
                count += 1            
        if count>1:
            return token
    for i in range(2,len(token)):
        word=""
        if token[i] in u and token[i-1] not in u:
            if token[i-1]=='h' or token[i-1]=="'":
                if token[i-2] in ['s','c']:
                    word+=token[0:i-2]+"-"+token[i-2:len(token)]
                else : word+=token[0:i-1]+"-"+token[i-1:len(token)]
            elif len(token[0:i-1])>1 : word+=token[0:i-1]+"-"+token[i-1:len(token)]
        if len(word)>1:
            w=word.split("-")
            if w[1][0]=='g' and w[0][len(w[0])-1] == 'n':
                s=w[1]
                w[1]='n'+s
                s=w[0]
                w[0]=s[0:len(s)-1]
            txt.append(w[0]+"-"+w[1])
    return txt

def count(text):
    tokens=syllables(text)
    count=0
    for token in tokens:
        syll=token.split('-')
        count+=len(syll)
    return count
