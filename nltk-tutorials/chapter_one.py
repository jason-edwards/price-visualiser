__author__ = 'jason'

"""
Notes on this tutorial reference.
Source: http://www.nltk.org/book/ch01.html
Ensure: using the nltk.download() window install the book collection. These
functions need this for the nltk.book module.

These are not intended to be used for future programs
"""

import nltk
import nltk.book as nltk_book


def main():
    section_one()


def section_one():
    # nltk_downloader()
    # print_titles()
    # monstrous_concordance()
    # monstrous_similar()
    # monstrous_common_context()
    # other_common_context()
    # text4_dispersion_plot()
    # text3_token_count()
    # text3_distinct_token_count()
    # text3_token_set()
    print(lexical_diversity(nltk_book.text3))
    print(token_density("smote", nltk_book.text3))


def print_titles():
    print(nltk_book.text1)
    print(nltk_book.text2)
    print('\n')


def monstrous_concordance():
    # The concordance method finds all references to argument with additional context.
    nltk_book.text1.concordance("monstrous")
    nltk_book.text2.concordance("monstrous")
    print('\n')


def monstrous_similar():
    # The similar method finds words that are used in a similar context.
    # i.e. Searching for similar containing the above sentence would look for
    # phrases that contain "a _____ context".
    # These will be different for different texts.
    nltk_book.text1.similar("monstrous")
    nltk_book.text2.similar("monstrous")
    print('\n')


def monstrous_common_context():
    # The common_context method shows the context shared by two or more words
    # Comparing monstrous to very in text2.
    nltk_book.text2.concordance("monstrous")
    nltk_book.text2.concordance("very")
    nltk_book.text2.common_contexts(["monstrous", "very"])
    print('\n')


def other_common_context():
    # See 'monstrous_common_context' for information
    nltk_book.text7.similar("finance")
    nltk_book.text7.concordance("finance")
    nltk_book.text7.concordance("visiting")
    nltk_book.text7.common_contexts(["finance", "visiting"])
    print('\n')


def text4_dispersion_plot():
    nltk_book.text4.dispersion_plot(["citizens", "democracy", "freedom",
                                     "duties", "America"])


def nltk_downloader():
    # Note: This window does not let you scroll on your keypad on a Macbook.
    nltk.download()
    print('\n')


def text3_token_count():
    # Counts the number of words in text3
    print(len(nltk_book.text3))
    print('\n')


def text3_distinct_token_count():
    # Counts the number of distinct words in text 3
    print(len(set(nltk_book.text3)))
    print('\n')


def text3_token_set():
    # A sorted list of all the unique tokens used in text3
    print(sorted(set(nltk_book.text3)))
    print('\n')


def lexical_diversity(nltk_text: nltk.text.Text) -> float:
    # Calculates (the inverse of) the frequency that tokens are repeated
    # in a specific text.
    token_distinct_count = len(set(nltk_text))
    token_count = len(nltk_text)
    print('\n')

    return token_distinct_count/token_count


def token_density(token: str, nltk_text: nltk.text.Text) -> float:
    # Calculates the frequency that a given token is repeated in a
    # specific text.
    token_frequency = nltk_text.count(token)
    text_length = len(nltk_text)
    print('\n')

    return token_frequency/text_length


if __name__ == "__main__":
    main()