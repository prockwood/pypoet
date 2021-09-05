import re
import numpy as np
from stopwords import stopwords
import sys



def clean(text):
    return text.lstrip().rstrip().split()


def make_word_count(word_list):
    word_list_unique = list(set(word_list))
    
    doc_dict = {}
    
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
    for word_dict in count_dict.keys():
        total = sum(count_dict[word_dict].values())
        for word in count_dict[word_dict].keys():
            count_dict[word_dict][word] = count_dict[word_dict][word]/total

    return count_dict


def choose_new_word(word, freq_dict):
    word_f_dict = freq_dict[word]
    probs = list(word_f_dict.values())
    keys = list(word_f_dict.keys())
    
    return str(np.random.choice(keys, 1, replace=True, p=probs)[0])


def make_line(start_word, line_length, freq_dict, color):
    poem = [start_word]
    for i in range(line_length):
        if poem[-1] not in freq_dict.keys():
            poem.append(poem[0])
        else:
            new_word = choose_new_word(poem[-1], freq_dict)
            poem.append(new_word)
    ppoem = poem.copy()
    
    def remove_trailing_stopwords(poem, stopwords):
        try:
            while poem[-1].lower() in stopwords:
    #             print('remove: ', poem[-1])
                poem.remove(poem[-1])
        except:
            poem = ['nothing', 'to', 'say']
        return poem
    
    ppoem = remove_trailing_stopwords(ppoem, stopwords)
#     print('post stopword removal ppoem: ', ppoem)
    
    
    ppoem[-1] = re.sub(r"[^a-zA-z]", '', ppoem[-1])   
    
    ppoem[0] = ppoem[0].capitalize()
    ppoem = [re.sub(r"[\“\”]", '', word) for word in ppoem]
    ppoem = [re.sub(r" +", '', word) for word in ppoem]
    ppoem = ' '.join(ppoem)
    ppoem = ppoem + '.'
#     print('\tpoem',poem)
    print('\t', color+ppoem+'\x1b[0m')
#     print('+++++++++++++++++++++++++++++++++++++++++++')
    return poem
    
def make_stanza(freq_dict, word_list, line_min, line_max):
    a = make_line(np.random.choice(word_list), 
              np.random.randint(line_min, line_max), 
              freq_dict,
              '\x1b[0m')
    
    b = make_line(a[-1], 
              np.random.randint(line_min, line_max), 
              freq_dict,
              '\x1b[0m')
    
    c = make_line(b[-1], 
              np.random.randint(line_min, line_max), 
              freq_dict,
              '\x1b[0m')
    print('')
    
def make_poem(text, line_min, line_max):
    freq_dict = count_to_freq_dict(make_word_count(clean(text)))
    word_list = list(freq_dict.keys())
    print('\n')
    make_line(np.random.choice(word_list), 
              np.random.randint(2, 3), 
              freq_dict,
              '\033[91m')
    print('--------------------------------------------------------------------\n')
    
    make_stanza(freq_dict, word_list, line_min, line_max)
    make_stanza(freq_dict, word_list, line_min, line_max)
    make_stanza(freq_dict, word_list, line_min, line_max)
    
    print('--------------------------------------------------------------------')
    print('\n')
    return 'end'
    

def main():     
    text_file = sys.argv[1]
    with open(text_file, 'r') as f:
        t = f.readlines()  
    mt = ' '.join(t)
    make_poem(mt, 2, 8)


if __name__ == '__main__':
    main()