"""Generate markov text from text files."""


from random import choice
import sys
import os
import twitter

api = twitter.Api(
    consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
    access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

print api.VerifyCredentials()

n = int(raw_input("What size would you like your n-grams to be? "))


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    f = open(file_path)

    text = f.read()

    f.close()

    return text


def make_chains(text_string, n):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
    """

    chains = {}

    words = text_string.split()

    for i in range(len(words) - (n - 1)):

        key = tuple(words[i:i + n])

        if key not in chains:
            chains[key] = []

        try:
            chains[key].append(words[i+n])
        except:
            chains[key].append(" ")

    return chains


def make_text(chains, n):
    """Returns text from chains."""

    words = []

    # CAPITALIZATION
    upper_chains = []

    for key in chains.keys():
        if key[0][0].isupper():
            upper_chains.append(key)

    # PUNCTUATION: not functional yet ???
    # ends_with_punct = []

    # for key in chains.keys():
    #     if key[-1][-1] == ".":
    #         ends_with_punct.append(key)

    current_key = choice(upper_chains)
    words.extend(current_key)

    words_length = len(" ".join(words))

    while words_length < 130:
        new_link = choice(chains[current_key])
        words.append(new_link)
        current_key = tuple(words[-n:])
        words_length = len(" ".join(words))
        if " " in chains[current_key]:
            break

    return " ".join(words)


def tweet(random_text):
    """ Posts status and asks user to send another tweet """

    while True:
        random_text = make_text(chains, n)
        status = api.PostUpdate(random_text)
        print random_text
        tweet_again = raw_input("Would you like to send another tweet? y/n: ")
        if tweet_again != "y":
            break


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n)

# Produce random text
random_text = make_text(chains, n)

tweet(random_text)
