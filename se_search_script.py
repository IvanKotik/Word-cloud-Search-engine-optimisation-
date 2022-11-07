import PyPDF2, os, re, time, requests
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
ps = PorterStemmer()

stopwords_list = {"i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this",'that',"that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"}


def input_sequence(input_initial): 

    '''Trimming input search terms to be used for the occurrence matrix. The output is a generalized stemmed input form ready for checking and a count of terms for the ngram_range.'''

    # splitting the phrase by pieces
    input_general = input_initial.split(' ')

    # cleaning stopwords
    input_general = [i for i in input_general if i not in stopwords_list]

    # count words
    input_general_count = len(input_general)

    # stem the words
    input_general = [ps.stem(i) for i in input_general]

    # create the additional variations of the phrase
    outer_list = []
    for i in range(0, input_general_count):
        inner_list = [input_general[j : input_general_count-i+j] for j in range(i+1)]
        outer_list.append(inner_list)

    return input_general, input_general_count, outer_list


def general_occurrence(input_general_count, combined_pdf): 

    '''Creation of the generalized tfidf occurance matrix based on dynamic parameters.'''

    vectorizer_general = TfidfVectorizer(smooth_idf=True, sublinear_tf=True, use_idf=True, lowercase=False, stop_words=stopwords_list, ngram_range=(input_general_count, input_general_count))
    X_general = vectorizer_general.fit_transform(combined_pdf)
    xx_general = pd.DataFrame(X_general.toarray(), columns = vectorizer_general.get_feature_names_out())
    return xx_general

def check_for_general(input_initial, input_general_count, outer_list, combined_pdf, number_of_urls):

    '''Main function.'''

    # initiating a breaker function
    breaker = 0
    # creating the occurrence matrix for max length
    xx_general = general_occurrence(input_general_count, combined_pdf)
    # creating an empty table for results
    test_output = xx_general.copy()
    test_output = test_output.iloc[:,0]*0
    # first test for full match
    print('search term: ', outer_list[0][0])
    test = ' '.join(outer_list[0][0])
    # if test passed
    if test in list(xx_general.columns):
        # create a ranked index
        ranked_indexes = xx_general[test].sort_values(ascending=False).index
        ranked_indexes = list(ranked_indexes[0:number_of_urls])
        # connect back to urls
        output_url = [q_master['id'][i] for i in ranked_indexes]
        print('search result: present\n')
        return output_url
    # if test failed drill-down
    else: 
        print('search result: not present, drill-down\n')
        for y in range(1, len(outer_list)):
            # create a new occurance matrix with new ngrams
            xx_general = general_occurrence(input_general_count-y, combined_pdf)
            for u in range(y+1):
                # drill-down phrase test
                print('search term: ', outer_list[y][u])
                test = ' '.join(outer_list[y][u])
                # if test passed
                if test in list(xx_general.columns):
                    # sum the tfidf indexes across multiple matches
                    test_output += xx_general[test]
                    print('search result: present\n')
                    # initiate the exit from the function
                    breaker = 1
                else: 
                    print('search result: not present\n')
            if breaker == 1:
                # order the indexes by highest tfidf
                ranked_indexes = test_output.sort_values(ascending=False).index
                ranked_indexes = list(ranked_indexes[0:number_of_urls])
                # return urls
                output_url = [q_master['id'][i] for i in ranked_indexes]
                return output_url


# search terms
input_initial = 'Pricing and hedging inverse BTC options'
number_of_urls = 5
# combined_pdf = ____

input_general, input_general_count, outer_list = input_sequence(input_initial)
output_url = check_for_general(input_initial, input_general_count, outer_list, combined_pdf, number_of_urls)
json_output = pd.DataFrame({'id': output_url}).to_json(orient='index')
print(json_output)