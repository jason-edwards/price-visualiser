__author__ = 'jason'

from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
import nltk
import numpy as np
import matplotlib.pyplot as plt
import random

# import nltk.book as nltk_book

def main() -> int:
    # section_one()
    # section_two()
    # section_four()
    # section_five()
    practice_questions()
    return 0


def section_one() -> int:
    print(nltk.corpus.gutenberg.fileids())
    print(token_counter(nltk.corpus.gutenberg.fileids()[0], "gutenberg"))
    corpus_file_info("webtext")
    corpus_file_info("nps_chat")

    return 0


def section_two() -> int:
    genres = ['news', 'government']
    cfd = cfd_genre_brown(genres)
    conditions = cfd.conditions()
    news_words = [tokens[0] for tokens in cfd['news'].most_common(20)]
    cfd.tabulate(conditions=conditions, samples=news_words, cumulative=True)
    print("----------------------------------------")
    government_words = [tokens[0] for tokens in cfd['government'].most_common(20)]
    cfd.tabulate(conditions=conditions, samples=government_words, cumulative=True)
    print("----------------------------------------")
    text = brown.words(brown.fileids()[0])
    bigrams = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams)
    generate_model(cfd, text[21])

    return 0


def section_four() -> int:
    print(unusual_words(brown.words()))
    return 0


def section_five() -> int:
    list_synsets('home')
    return 0


def practice_questions() -> int:
    # zipf_law(brown.words())
    random_text = random_text_gen(5000000)
    zipf_law(random_text)
    return 0


def random_text_gen(len: int) -> str:

    string = ''
    for index in range(len):
        string += random.choice("abcdefghijkl ")

    text = string.split(' ')
    return text


def zipf_law(text: list) -> int:
    fdist = nltk.FreqDist(text)
    sorted_list = sorted(fdist.values(), reverse=True)
    ln_x = [np.log(x) for x in range(1, len(sorted_list)+1)]
    plt.plot(ln_x, sorted_list)
    ln_sorted_list = [np.log(y) for y in sorted_list]
    # plt.plot(ln_sorted_list)
    plt.show()
    return 0


def list_synsets(token: str) -> int:
    for synset in wn.synsets(token):
        print(synset.lemma_names())

    return 0


def unusual_words(text: list) -> list:
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)


def generate_model(cfdist, word, num=15) -> int:
    for i in range(num):
        print(word, end=' ')
        word = cfdist[word].max()

    return 0

def cfd_genre_brown(genres: list) -> int:
    genre_word = []
    for genre in genres:
        for word in brown.words(categories=genre):
            genre_word.append((genre, word))
    cfd = nltk.ConditionalFreqDist(genre_word)
    return cfd


def token_counter(file_name: str, corpus: PlaintextCorpusReader) -> int:
    corpora = nltk.corpus.__getattr__(corpus)
    token_count = len(corpora.words(file_name))
    return token_count


def corpus_file_info(corpus: PlaintextCorpusReader) -> int:
    corpora = nltk.corpus.__getattr__(corpus)

    for fileid in corpora.fileids():
        num_chars = len(corpora.raw(fileid))
        num_words = len(corpora.words(fileid))
        num_vocab = len(set(w.lower() for w in corpora.words(fileid)))
        try:
            num_sents = len(corpora.sents(fileid))
            print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)
            break
        except AttributeError:
            print(round(num_chars/num_words), "N/A", round(num_words/num_vocab), fileid)
    return 0

if __name__ == '__main__':
    main()