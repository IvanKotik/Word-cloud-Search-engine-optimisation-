import PyPDF2, os, re, time, requests
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
ps = PorterStemmer()

# generic stop words list, done like this to be independent of packages
stopwords_list = {"i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this",'that',"that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't", "udcurlymod", "nvcpinkrddstratxbcbtsburstdgbdogeltcardrgntlskpascxrpbtcetcethomniscdashdcrfctgnonmrdynam", "btcomnigntclambbrdgbsclsknmrblitzltcethbtsfctdogestratsteembtcddmdbtmgroup", "vydytiyzjjhrtncozhjtzv", "vbuptqjymgcq", "leiowsmcwqueca", "uicgnihcgj", "hfd", "honxnk", "latexit", "latexit", "sha", "base", "nqu", "xkgewckhjywtkfomismnzuo", "aaab" ,"nicbzbnswmxeizn", "rr", "ainsqucoqt", "mvjbfsb", "vjm", "wbm", "gjcuupt", "ciwdfvpp", "vplvtn", "aoslgyd", "zsjmgynbjfx", "tfwnza", "rbwdt", "yaacqanbwp", "kromocsn", "gnwuzphegrwj", "vbuptqjymgcq", "ljtte", "douzi", "leqf", "xcueavcjx", "eikvzwqslao", "pbr", "yyy", "acirytnzldfnixzhkxycs", "bcfl", "uljw", "divlsnlzm", "vydytiyzjjhrtncozhjtzv", "vglzllvmmaslj", "jmeju", "kwdwjvkwcinxc", "urocdv", "latexit", "null", "sha"}


def input_sequence(input_initial): 

    '''Trimming input search terms to be used for the occurrence matrix. The output is a generalized stemmed input form ready for checking and a count of terms for the ngram_range.'''

    # splitting the phrase by pieces
    search_term = input_initial.split(' ')

    # cleaning stopwords
    search_term = [i for i in search_term if i not in stopwords_list]

    # count words
    search_term_count = len(search_term)

    # stem the words
    search_term = [ps.stem(i) for i in search_term]

    # create the additional variations of the phrase
    outer_list = []
    for i in range(0, search_term_count):
        inner_list = [search_term[j : search_term_count-i+j] for j in range(i+1)]
        outer_list.append(inner_list)

    return search_term, search_term_count, outer_list


def general_occurrence(search_term_count, combined_pdf): 

    '''Creation of the generalized tfidf occurance matrix based on dynamic parameters.'''

    vectorizer_general = TfidfVectorizer(smooth_idf=True, sublinear_tf=True, use_idf=True, lowercase=False, stop_words=stopwords_list, ngram_range=(search_term_count, search_term_count))
    X_general = vectorizer_general.fit_transform(combined_pdf)
    xx_general = pd.DataFrame(X_general.toarray(), columns = vectorizer_general.get_feature_names_out())
    return xx_general

def check_for_general(search_term, q_master, search_term_count, outer_list, combined_pdf, number_of_urls):

    '''Main function.'''

    # initiating a breaker function
    breaker = 0

    # creating a list out of the pdf-json
    combined_pdf = [combined_pdf[str(i)]['text'] for i in range(len(combined_pdf))]

    # creating the occurrence matrix for max length
    xx_general = general_occurrence(search_term_count, combined_pdf)

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
            xx_general = general_occurrence(search_term_count-y, combined_pdf)
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

# how many outputs are needed
number_of_urls = 5

##################################################################################################
# this section should be run from se_pdfdownloader.py

# fetching all pdfs from a json file stored in web
url_text = 'https://raw.githubusercontent.com/IvanKotik/Word-cloud-Search-engine-optimisation-/419447491efef2bb3a21b0459e5bdcd352a39097/combined_pdf_json.json'
r = requests.get(url_text)
combined_pdf = r.json()

# fetching previous quantinar meta master list, i.e. all the id's and the links
url_master = 'https://raw.githubusercontent.com/IvanKotik/Word-cloud-Search-engine-optimisation-/master/q-master-json.json'
e = requests.get(url_master)
q_master_json = e.json()


# converting the master meta list to a dataframe
q_master = pd.DataFrame({'id' : [q_master_json[str(i)]['id'] for i in range(len(q_master_json))],
'name' : [q_master_json[str(i)]['name'] for i in range(len(q_master_json))],
'team' : [q_master_json[str(i)]['team'] for i in range(len(q_master_json))],
'artist' : [q_master_json[str(i)]['artist'] for i in range(len(q_master_json))],
'author' : [q_master_json[str(i)]['author'] for i in range(len(q_master_json))],
'published_in' : [q_master_json[str(i)]['published_in'] for i in range(len(q_master_json))],
'full_link' : [q_master_json[str(i)]['full_link'] for i in range(len(q_master_json))],
'pdf_url' : [q_master_json[str(i)]['pdf_url'] for i in range(len(q_master_json))]
})
# filtering out all the quantlets that we do not have a link associated with from metadata
q_master['url_check'] = [len(i) for i in q_master['pdf_url']]
q_master = q_master.loc[q_master['url_check'] != 0, ]
q_master = q_master.reset_index(drop=True)
##################################################################################################


search_term, search_term_count, outer_list = input_sequence(input_initial)
output_url = check_for_general(search_term, q_master, search_term_count, outer_list, combined_pdf, number_of_urls)
json_output = pd.DataFrame({'id': output_url}).to_json(orient='index')
print(json_output)