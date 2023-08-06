import os,sys
from fileinput import FileInput as finput

bib = sys.argv[1:]

def any_kar_capital(string):
    for kar in string:
        if kar.isupper():
            return True
    return False


# https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

with finput(bib,inplace=True,backup=None) as foil:
    for line in foil:
        if line.strip().startswith('title'):
            stub=[]
            line = line.replace('title','',1).strip().replace('=','').strip().replace('{','',1).strip()# [:-1]
            line = rreplace(line,'}','',1)
            line = rreplace(line,',','',1)
            for word in line.split(' '):
                if any_kar_capital(word):
                    stub += ["{"+str(word)+'}']
                else:
                    stub += [str(word)]
            line = "title={"+' '.join(stub) +'},\n'

        print(line,end='')

print('Finished')
