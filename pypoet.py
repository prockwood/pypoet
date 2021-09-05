import re
import numpy as np
from stopwords import stopwords
import sys


def clean(text):
    """Strip white space from ends and listify a string."""
    return text.lstrip().rstrip().split()


def make_word_count(word_list):
    """
    Take list of strings, make a dict of proceeding string frequencies
    for each string.
    """
    # Container for our word count dict.
    doc_dict = {}
    # For each word, make a dict of the counts of each proceeding word.
    for i in range(len(word_list) - 1):
        if word_list[i] in doc_dict.keys():
            if word_list[i+1] in doc_dict[word_list[i]].keys():
                doc_dict[word_list[i]][word_list[i+1]] += 1
            else:
                doc_dict[word_list[i]][word_list[i+1]] = 1
        else:
            doc_dict[word_list[i]] = {word_list[i+1]: 1}
    return doc_dict


def count_to_freq_dict(count_dict):
    """Convert counts to frequencies"""
    for word_dict in count_dict.keys():
        total = sum(count_dict[word_dict].values())
        for word in count_dict[word_dict].keys():
            count_dict[word_dict][word] = count_dict[word_dict][word]/total

    return count_dict


def choose_new_word(word, freq_dict):
    """Generate a new word from the frequency dict."""
    word_f_dict = freq_dict[word]
    probs = list(word_f_dict.values())
    keys = list(word_f_dict.keys())
    # Use numpy random.choice with keys and probs.
    return str(np.random.choice(keys, 1, replace=True, p=probs)[0])


def make_line(start_word, line_length, freq_dict, color):
    """Make a line of poetry."""
    # Initialize with a word from the dict.
    poem = [start_word]
    # Append new word if start word in dict.
    for i in range(line_length):
        if poem[-1] not in freq_dict.keys():
            poem.append(poem[0])
        else:
            new_word = choose_new_word(poem[-1], freq_dict)
            poem.append(new_word)
    ppoem = poem.copy()

    def remove_trailing_stopwords(poem, stopwords):
        """Remove stop words from end of line for better parsability."""
        try:
            while poem[-1].lower() in stopwords:
                poem.remove(poem[-1])
        except IndexError:
            poem = ['nothing', 'to', 'say']
        return poem

    # Formating and cleaning
    ppoem = remove_trailing_stopwords(ppoem, stopwords)
    ppoem[-1] = re.sub(r"[^a-zA-z]", '', ppoem[-1])
    ppoem[0] = ppoem[0].capitalize()
    ppoem = [re.sub(r"[\“\”]", '', word) for word in ppoem]
    ppoem = [re.sub(r" +", '', word) for word in ppoem]
    # list to string, add period, print line
    ppoem = ' '.join(ppoem)
    ppoem = ppoem + '.'
    print('\t', color+ppoem+'\x1b[0m')
    return poem


def make_stanza(freq_dict, word_list, line_min, line_max):
    """Make a 3 line stanza from make_line calls."""
    # First line with random word from dict
    a = make_line(np.random.choice(word_list),
                  np.random.randint(line_min, line_max),
                  freq_dict,
                  '\x1b[0m')
    # Second and third lines use last word of last line as first word.
    b = make_line(a[-1],
                  np.random.randint(line_min, line_max),
                  freq_dict,
                  '\x1b[0m')  # normal white color
                              # https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007

    c = make_line(b[-1],
                  np.random.randint(line_min, line_max),
                  freq_dict,
                  '\x1b[0m')
    print('')


def make_poem(text, line_min, line_max):
    """Integrate above functions to print 3 stanzas."""
    freq_dict = count_to_freq_dict(make_word_count(clean(text)))
    word_list = list(freq_dict.keys())
    print('\n')
    make_line(np.random.choice(word_list),
              np.random.randint(2, 3),
              freq_dict,
              '\033[91m')
    print('----------------------------------------------------------------\n')
    make_stanza(freq_dict, word_list, line_min, line_max)
    make_stanza(freq_dict, word_list, line_min, line_max)
    make_stanza(freq_dict, word_list, line_min, line_max)
    print('----------------------------------------------------------------')
    print('\n')
    return 'end'


def main():
    """Open Text file call make_poem."""
    text_file = sys.argv[1]
    with open(text_file, 'r') as f:
        t = f.readlines()
    mt = ' '.join(t)
    make_poem(mt, 2, 8)


if __name__ == '__main__':
    main()
