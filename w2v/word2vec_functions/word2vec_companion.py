import json
from gensim.models import Word2Vec
from .text_processing_functions import all_processing


def preprocess_wordlist(word_list, print_on=True):
    '''
    Accepts a list of individual words and runs them through the pre-processing so they can be fed to the Word2Vec model
    Can potentially return an empty list.
    '''
    if type(word_list) != list:
        raise ValueError('Input to preprocess_wordlist must be a list of individual words')
    
    processed_words = []
    
    for word in word_list:
        processed_list = all_processing(word)[0]
        
        if not processed_list:
            if print_on:
                print(f"'{word}' is removed from the data during initial pre-processing")
        else:
            processed_words.append(processed_list[0])
    
    return processed_words


def in_corpus_vocab(cleaned_list, corpus_vocab, print_on=True):
    '''
    Accepts a list of words that have been preprocessed
    Returns a smaller list of the words which appeared in the corpus
    '''
    
    cleaned_words_in_corpus = []
    for cleaned_word in cleaned_list:
        if cleaned_word not in corpus_vocab.keys():
            if print_on:
                print(f"'{cleaned_word}' does not appear in the processed corpus")
        else:
            cleaned_words_in_corpus.append(cleaned_word)
    
    return cleaned_words_in_corpus


def remove_uncommon(cleaned_list, corpus_vocab, occurrence_threshold = 10, print_on = True):
    '''
    Accepts a list of preprocessed words. Checks the corpus vocab and removes words which
    do not meet a minimum occurrence threshold.
    Returns a list of words.
    May return an empty list.
    '''
    
    cleaned_words_common = []
    for cleaned_word in cleaned_list:
        total_occurrences = 0
        
        for translated_word in corpus_vocab[cleaned_word].keys():
            total_occurrences += corpus_vocab[cleaned_word][translated_word]
        
        if total_occurrences > occurrence_threshold:
            cleaned_words_common.append(cleaned_word)
        else:
            if print_on:
                print(f"'{cleaned_word}' appears in the corpus {total_occurrences} times, which is less than the threshold of {occurrence_threshold} times")
    
    return cleaned_words_common

def clean_user_input(word_list, preprocess_text):
    # some input text might already be preprocessed. You can't double preprocess because double stemming can occur
    if preprocess_text:
        # preprocess all the input words
        cleaned_list = preprocess_wordlist(word_list, print_on=True)
        if not cleaned_list:
            print('All words were removed during preprocessing')
            return None
    else:
        cleaned_list = word_list    

    return cleaned_list


def remove_non_corpus_words(cleaned_list, occurrence_threshold, corpus_vocab):
    
    # remove words that do not appear in the corpus
    cleaned_list = in_corpus_vocab(cleaned_list, corpus_vocab, print_on = True)
    if not cleaned_list:
        print('None of the processed words appear in the processed corpus')
        return None
    
    # remove words which don't meet an occurrence threshold
    cleaned_list = remove_uncommon(cleaned_list, corpus_vocab, occurrence_threshold, print_on = True)
    if not cleaned_list:
        print('None of the processed words were common enough to be considered')
        return None

    return cleaned_list


def similar_words(positive_word_list, negative_word_list, corpus_vocab, model, verbose = True, occurrence_threshold = 10, preprocess_text = True, words_returned = 10, limited_vocabulary = None):
    '''The occurrence cutoff will limit results to words that occurred in the corpus more often than the cutoff.
    Corpus vocab is all of the translations.
    '''

    positive_word_list = clean_user_input(positive_word_list, preprocess_text)
    positive_word_list = remove_non_corpus_words(positive_word_list, occurrence_threshold, corpus_vocab) 

    if negative_word_list:
        print('this should not have run')
        negative_word_list = clean_user_input(negative_word_list, preprocess_text)
        negative_word_list = remove_non_corpus_words(negative_word_list, occurrence_threshold, corpus_vocab)
    else:
        negative_word_list = None
        
    # TODO: add a handler if none of the words are in the vocab
    
    ########################################################################################### 

    # check if the user wants to filter the results on a certain vocabulary
    if limited_vocabulary:

        # process the limited vocab and split compound words into their parts #TODO figure out how to handle compounds        
        first_pass = [all_processing(word)[0] for word in limited_vocabulary]
        limited_vocab_processed = []
        for item in first_pass:
            if item:
                for word in item:
                    limited_vocab_processed.append(word)        

        results = model.wv.most_similar(positive=positive_word_list, negative=negative_word_list, topn = len(model.wv.vocab))

        results = [result for result in results if result[0] in limited_vocab_processed]

        # will prevent an index error if there aren't enough results
        if words_returned > len(results):
            words_returned = len(results)

        results = results[:words_returned]
    else:
        
        results = model.wv.most_similar(positive=positive_word_list, negative=negative_word_list, topn = words_returned)

    translated_results = []
    for rank, result in enumerate(results):

        match = result[0]
        match_score = result[1]
        match_translations = corpus_vocab[match]
        top_translation = max(match_translations.keys(), key=(lambda key: match_translations[key]))

        if verbose:
            print('Exact Match', rank, ':', match)
            print('Score:', match_score)
            print('Top Translation:', top_translation)
            print('---------- All Translations -----------')
            print(match_translations)
            print('=======================================================\n')
        elif not verbose:
            print('Score:', round(match_score,2), '  Match:', top_translation)
    
        translated_results.append((top_translation, match_score))

    return translated_results #results

