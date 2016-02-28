import nltk
from nltk.corpus import webtext
import random
import matplotlib.pyplot as plt
import numpy

alphabet = 'abcdefghijklmnopqrstuvwxyz'
#c = 500000

#random_string = ''
#for i in range(c):
#    random_string += random.choice(alphabet + ' ')

##fdist = nltk.FreqDist(random_string.split())
#fdist = nltk.FreqDist(book.text1)
#sortedvalues = sorted(fdist.values(), reverse=True)
#lnrange = [numpy.log10(x) for x in range(1, len(sortedvalues)+1)]

#print(fdist.most_common(50))

#plt.plot(lnrange, sortedvalues)
#plt.show()


def generate_model(cfdist, word, n, num):
    for i in range(num):
        print(word, end=' ')
        #word = cfdist[word].max()
        ncommonwords = cfdist[word].most_common(n)
        if len(ncommonwords) == 0:
            print("<Ran out of words!>")
            break
        word = random.choice(ncommonwords)[0]

#text = webtext.words()
def shit_talk(friendname, seedword, n=3, num=50):
    with open("Shit %s Says.txt" % friendname, encoding='utf8') as f:
        rawtext = f.read()
        text = nltk.tokenize.casual_tokenize(rawtext)
    lowercasetext = [i.lower() for i in text]

    filteredtokens = []
    for w in lowercasetext:
        if w[0] in alphabet:
            filteredtokens.append(w)

    bigrams = nltk.bigrams(filteredtokens)
    cfd = nltk.ConditionalFreqDist(bigrams)

    generate_model(cfd, seedword, n, num)
