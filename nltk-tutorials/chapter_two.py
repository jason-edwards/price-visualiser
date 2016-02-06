__author__ = 'jason'

import nltk
# import nltk.book as nltk_book

def main() -> int:
    section_one()
    return 0


def section_one() -> int:
    print(nltk.corpus.gutenberg.fileids())
    print(token_counter(nltk.corpus.gutenberg.fileids()[0], "gutenberg"))
    corpus_file_info("webtext")
    corpus_file_info("nps_chat")

    return 0


def token_counter(
        file_name: str,
        corpus: nltk.corpus.reader.plaintext.PlaintextCorpusReader
        ) -> int:
    corpora = nltk.corpus.__getattr__(corpus)
    token_count = len(corpora.words(file_name))
    return token_count


def corpus_file_info(
        corpus: nltk.corpus.reader.plaintext.PlaintextCorpusReader
        ) -> int:
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