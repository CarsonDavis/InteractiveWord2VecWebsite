import re
import contractions
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from stemming import porter2  # lovins, paicehusk


def to_lowercase(text):
    return text.lower()


def convert_spaces(text):
    return re.sub(r'\s', ' ', text)


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_internal_punctuation(text):
    """converts internal punctuation (not '.'s) to spaces where necessary (man-bear-pig => man bear pig)"""
    return re.sub(r'(?<=[a-zA-Z])[^a-zA-Z0-9.]+(?=[a-zA-Z])', ' ', text)


def remove_all_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)


def replace_numbers(text):
    """replaces sequences of numbers with the string 'number' """
    return re.sub(r'\d+', 'number', text)


def to_vector(text):
    return text.split()


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def split_units(words):
    """previous processing results in units being appended to the end of the string 'number' this function splits
    them apart. Example (15cm -> numbercm -> number cm)"""
    new_words = []
    for word in words:
        if 'number' in word and len(word) != 6:
            word = ['number', word[6:]]
            new_words += word
        else:
            new_words.append(word)
    
    return new_words


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""

    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for index, word in enumerate(words):
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


def stem_lancaster(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def stem_porter2(words):
    """Stem words in list of tokenized words"""
    stemmer = porter2
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def build_translation(raw_wordlist, processed_wordlist):
    """
    when words are stemmed, multiple different words can resolve to a single stemmed word. this function monitors the
    stemming and lemmatization process to keep a record of the frequency for each stem so a translation can be made later
    :param raw_wordlist: ordered list of words before stemming and lemmatization
    :param processed_wordlist:
    :return: {processed : {raw_1: count, raw_2: count}
    """

    stem_translation = {}
    for index, processed_word in enumerate(processed_wordlist):

        stem_translation[processed_word] = stem_translation.get(processed_word, {})
        stem_translation[processed_word][raw_wordlist[index]] = stem_translation[processed_word].get(raw_wordlist[index],0)
        stem_translation[processed_word][raw_wordlist[index]] += 1

    return stem_translation


def all_processing(text):
    """
    all_processing() runs all of the pre-processing steps at once
    :param text: accepts a string of text
    :return: returns a BoW of processed text, as well as a record of all stem translations
    """

    text = to_lowercase(text)
    text = replace_contractions(text)
    # TODO: identify and replace websites and emails
    text = remove_internal_punctuation(text)
    text = remove_all_punctuation(text)
    text = replace_numbers(text)
    words_orig = to_vector(text)
    words_orig = remove_stopwords(words_orig)
    words_orig = split_units(words_orig)

    words_new = words_orig.copy()
    
    words_new = lemmatize_verbs(words_new)
    words_new = stem_porter2(words_new)

    stem_translation = build_translation(words_orig, words_new)
    
    return [words_new, stem_translation]


def all_processing_troubleshooting(text, print_on = False):
    """
    all_processing_troubleshooting() runs all of the pre-processing steps at once. it also prints out the
    processing at each step so the programmer can troubleshoot the code
    :param text: accepts a string of text
    :return: returns a BoW of processed text, as well as a record of all stem translations
    """
    
    if print_on: print('Original:      ', text, '\n')
    
    text = to_lowercase(text)
    if print_on: print('Lowercase:     ', text)
    
    text = replace_contractions(text)
    if print_on: print('Contractions:  ', text)
    
    text = remove_internal_punctuation(text)
    if print_on: print('Internal Punc: ', text)
    
    text = remove_all_punctuation(text)
    if print_on: print('All Punc:      ', text)
    
    text = replace_numbers(text)
    if print_on: print('Numbers:       ', text)

    if print_on: print()
    
    words = to_vector(text)
    if print_on: print('Vector:    ', words,'\n')
    
    words = remove_stopwords(words)
    if print_on: print('Stopwords  ', words, '\n')
   
    words = split_units(words)
    if print_on: print('Split Num ', words, '\n')

    words = lemmatize_verbs(words)
    if print_on: print('Lemmatize: ', words, '\n')
    
    words = stem_porter2(words) 
    if print_on: print('Stem:      ', words, '\n') 

    return words
