# from .word2vec_functions.text_processing_functions import *
from .word2vec_functions.word2vec_companion import similar_words
from gensim.models import Word2Vec
import json

BASE_PATH = 'w2v/word2vec_functions/'

def load_filters():

    with open(BASE_PATH + 'Raw Data/test_data.json', 'r') as file:
        test_data = json.load(file)

    # abstract = test_data['test_abstract']
    # paper = test_data['test_paper']
    sweet_words = test_data['sweet_words']
    sweet_dict = test_data['sweet_dict']

    sweet_dict['all'] = sweet_words

    instrument_types = test_data['instrument_types']    

    filters = sweet_dict
    filters['instruments'] = instrument_types
    # filters = {'instruments': instrument_types, 
    #            'all': sweet_dict}

    return filters

def load_models():

    model = Word2Vec.load(BASE_PATH + 'Trained Models/model_e300_s150_w10_m3.model')
    tuple_model = Word2Vec.load(BASE_PATH + 'Trained Models/TupleExtractions_e300_s150_w10_m3.model')

    models = {'traditional': model,
              'tuple': tuple_model}
    
    return models

def load_translations():

    with open(BASE_PATH + 'Processed Training Data/papers_translations.json', 'r') as file:
        translations = json.load(file)
        
    return translations

def similar_word_list_wrapper(positive_words, negative_words, filter_vocab):
    filters = load_filters()
    models = load_models() 
    translations = load_translations()

    model = models['traditional']
    print('positive words', positive_words)
    print('negative words', negative_words)
    print(filter_vocab)
    
    similar_word_list = similar_words(positive_words, negative_words, translations, model, 
                                      verbose = False, 
                                      words_returned = 20, 
                                      limited_vocabulary = filter_vocab)

    return similar_word_list
