import pandas as pd
from text_processing_functions import all_processing
import multiprocessing
from time import time
import json
import os
import codecs


# it might be possible to shorten or remove this function if the multiprocessing library
# call can be modified to unpack an internal function output.
def unpack_data(data):
    """
    This function will flatten all the words from all the paper into one
    list. It will also take all the translations and flatten them into one master dictionary.
    """

    all_words = []
    all_translations = {}

    for paper in data:
        
        words = paper[0]
        translations = paper[1]
        
        all_words.append(words)
        
        for new_word in translations.keys():
            all_translations[new_word] = all_translations.get(new_word,{})
            
            for original_word in translations[new_word].keys():
                all_translations[new_word][original_word] = all_translations[new_word].get(original_word, 0)
                all_translations[new_word][original_word] += translations[new_word][original_word]    
    
    return all_words, all_translations


def ingest_csv(file_path='Raw Data/papers__corpus_22k_accessed_2019-02-07.csv'):
    """
    this function is designed to ingests the csv sent from Alex. This csv data is suboptimal because
    of the weird encoding that resulted in '-'s being encoded as 'a's, among other issues
    """

    papers = pd.read_csv(file_path, sep='\t')

    # about 214 papers had no text in the abstract or the main_body. this will remove those documents
    original_len = len(papers)
    papers['full_text'] = papers['Abstract'] + ' ' + papers['mainbody_clean']
    papers = papers[papers['full_text'].apply(lambda x: type(x) == str)]
    print(original_len-len(papers), 'papers removed for having no text')

    papers_text = list(papers['full_text'])  # convert column into list for processing

    return papers_text


def ingest_json(folder_path, test_run=False):
    """
    the papers in the corpus are stored as JSON files
    this function iterates over a folder and reads every json file
    it outputs a list with each element being the BoW of either an abstract or a fulltext
    """

    # TODO: modify so that abstracts and main bodies are combined so each element is a paper+abstract

    file_paths = []
    text_data = []
    file_count = 0
    error_count = 0

    for file_path in os.listdir(folder_path):
        if file_path.endswith('.json'):
            file_paths.append(os.path.join(folder_path, file_path))

    for file_path in file_paths:
        try:
            with codecs.open(file_path, 'r', 'utf-8') as file:
                data = json.load(file)

                if data['abstract']:
                    text_data.append(data['abstract'])

                if data['fulltext']:
                    text_data.append(data['fulltext'])

            file_count += 1
            if file_count > 500 and test_run:
                print('Test run complete')
                print('There were errors reading', error_count, 'papers.')
                return text_data

        except:  # TODO log error information in a file
            error_count += 1

    # about 40 papers of 22k are failing as of 5/21/19
    print('There were errors reading', error_count, 'papers.')
    return text_data


def main():

    # papers = ingest_csv()
    papers = ingest_json('journal_extractions')

    start = time()

    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=16)
    # papers_processed, papers_translations = pool.map(all_processing, batch_one)
    data = pool.map(all_processing, papers)
    pool.close()

    end = time()
    print("Time to process", end-start)
    
    #################################################################
   
    return data  # (papers_processed, papers_translations)


if __name__ == '__main__':
    processed_data = main()

    processed_papers, stem_translations = unpack_data(processed_data)

    with open('Processed Training Data/papers_processed.json', 'w') as file:
        json.dump(processed_papers, file)

    with open('Processed Training Data/papers_translations.json', 'w') as file:
        json.dump(stem_translations, file)
