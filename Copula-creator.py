import PyPDF2
import re
import requests
import pandas as pd
from itertools import combinations 
from itertools import permutations
from itertools import chain

# id_naming
id_num = 1
id_pdf = "id-{}".format(id_num)

def download_pdf(url, file_name, headers):
    '''Download a PDF file with an URL (Step 1)'''
    response = requests.get(url, headers=headers)
    # if response is OK download the PDF and store it, else write the status
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)
    return

def create_string(file_name):
    '''Transform a PDF file to a list of string pages (Step 2)'''
    # opening the file
    imported_pdf = open(file_name, 'rb')
    # convert PDF to readable file
    transformed_pdf = PyPDF2.PdfFileReader(imported_pdf)
    # get number of pages
    totalpages = transformed_pdf.numPages
    # read the data and store in a list
    pdf_output = [transformed_pdf.getPage(i) for i in range(totalpages)]
    # extract result
    pdf_output = [pdf_output[i].extractText() for i in range(totalpages)]
    return pdf_output, totalpages 


def cleaning(file_name):
    '''Initial PDF cleaning procedure (Step 3)'''
    pdf_output, totalpages = create_string(file_name)
    # cleaning URLs
    pdf_output = [re.sub(pattern = "http[^ ]*", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    # cleaning symbols
    pdf_output = [re.sub(pattern = "(\)|\(|,|\.|!|=|:|\[|\]|\{|\}|\'|\"|#|<|>|\%|\&|\?|\*|\/|-|\$|\+|\d)", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    # cleaning multispaces
    pdf_output = [re.sub(pattern = "\s{2,}", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    # cleaning out 1-worders
    pdf_output = [re.sub(pattern = " \w ", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    # lower-casing
    pdf_output = [pdf_output[i].lower() for i in range(totalpages)]
    return pdf_output, totalpages


def word_lists(file_name):
    '''Creating the base one-word, two-word and three-word lists, the permutation lists for two- and three-word lists (Step 4)'''
    pdf_output, totalpages = cleaning(file_name)
    # split to a list
    word_list = [pdf_output[i].split(" ") for i in range(totalpages)]
    # converting to a dataframe
    word_list = pd.DataFrame(word_list)
    # one-word section
    one_word_list = [word_list.iloc[j, i] for j in range(totalpages) for i in range(len(word_list))]
    # two-word section
    two_word_list = [[word_list.iloc[j, i], word_list.iloc[j, i+1]] for j in range(totalpages)  for i in range(len(word_list) - 1)]
    two_word_permutation_list = [[p for p in permutations(two_word_list[k])][1:] for k in range(len(two_word_list))]
    two_word_permutation_set = set(list(chain(*two_word_permutation_list)))
    # three-word section
    three_word_list = [[word_list.iloc[j, i], word_list.iloc[j, i+1], word_list.iloc[j, i+2]] for j in range(totalpages) for i in range(len(word_list) - 2)]
    three_word_permutation_list = [[p for p in permutations(three_word_list[k])][1:] for k in range(len(three_word_list))]
    three_word_permutation_set = set(list(chain(*three_word_permutation_list)))
    return word_list, one_word_list, two_word_list, two_word_permutation_list, two_word_permutation_set, three_word_list, three_word_permutation_list, three_word_permutation_set


def occurrance_three_matrix_creator(file_name):
    '''Creating the occurrance matrices for the three-word lists (Step 5)'''
    word_list, one_word_list, two_word_list, two_word_permutation_list, two_word_permutation_set, three_word_list, three_word_permutation_list, three_word_permutation_set = word_lists(file_name)
    # copying the data
    words = three_word_list.copy()
    # converting to a dataframe
    words = pd.DataFrame(three_word_list)
    # creating the three-word combinations as one string
    words = [words.iloc[i,0] + " " + words.iloc[i,1] + " " + words.iloc[i,2] for i in range(len(three_word_list)) if words.iloc[i,].isna().any() == False]
    # crating the dictionary
    dictionary_three_word = dict()
    
    # counting word occurances
    for word in words:
        if word in dictionary_three_word:
            dictionary_three_word[word] = dictionary_three_word[word] + 1
        else:
            dictionary_three_word[word] = 1
    
    # creating the occurance matrix
    dictionary_three_words = dictionary_three_word.items()
    dictionary_three_list = list(dictionary_three_words)
    occurrence_three_matrix = pd.DataFrame(dictionary_three_list)
    occurrence_three_matrix = occurrence_three_matrix.rename(columns={0:"word", 1:"occurance"})
    
    # clean of NaNs
    occurrence_three_matrix = occurrence_three_matrix.loc[occurrence_three_matrix.word.isna() == False, ]
    occurrence_three_matrix = occurrence_three_matrix.loc[occurrence_three_matrix.word != "None", ]

    # sort values
    occurrence_three_matrix = occurrence_three_matrix.sort_values("occurance", ascending=False)

    # re-indexing
    occurrence_three_matrix['index'] = range(len(occurrence_three_matrix))
    occurrence_three_matrix = occurrence_three_matrix.set_index('index')
    return occurrence_three_matrix


def occurrance_two_matrix_creator(file_name):
    '''Creating the occurrance matrices for the two-word lists (Step 6)'''
    word_list, one_word_list, two_word_list, two_word_permutation_list, two_word_permutation_set, three_word_list, three_word_permutation_list, three_word_permutation_set = word_lists(file_name)
    # copying the data
    words = two_word_list.copy()
    # converting to a dataframe
    words = pd.DataFrame(two_word_list)
    # creating the three-word combinations as one string
    words = [words.iloc[i,0] + " " + words.iloc[i,1] for i in range(len(two_word_list)) if words.iloc[i,].isna().any() == False]
    # crating the dictionary
    dictionary_two_word = dict()
    
    # counting word occurances
    for word in words:
        if word in dictionary_two_word:
            dictionary_two_word[word] = dictionary_two_word[word] + 1
        else:
            dictionary_two_word[word] = 1
    
    # creating the occurance matrix
    dictionary_two_words = dictionary_two_word.items()
    dictionary_three_list = list(dictionary_two_words)
    occurrence_two_matrix = pd.DataFrame(dictionary_three_list)
    occurrence_two_matrix = occurrence_two_matrix.rename(columns={0:"word", 1:"occurance"})
    
    # clean of NaNs
    occurrence_two_matrix = occurrence_two_matrix.loc[occurrence_two_matrix.word.isna() == False, ]
    occurrence_two_matrix = occurrence_two_matrix.loc[occurrence_two_matrix.word != "None", ]

    # sort values
    occurrence_two_matrix = occurrence_two_matrix.sort_values("occurance", ascending=False)

    # re-indexing
    occurrence_two_matrix['index'] = range(len(occurrence_two_matrix))
    occurrence_two_matrix = occurrence_two_matrix.set_index('index')
    return occurrence_two_matrix


def occurance_one_matrix_creator(file_name):
    '''Creating the occurrance matrix for one-word combinations (Step 7)'''
    word_list, one_word_list, two_word_list, two_word_permutation_list, two_word_permutation_set, three_word_list, three_word_permutation_list, three_word_permutation_set = word_lists(file_name)
    # copying the data
    words = one_word_list.copy()
    # creating the three-word combinations as one string
    words = [x for x in words if x != ""]
    words = [x for x in words if x != " "]    
    # crating the dictionary
    dictionary_one_word = dict()
    
    # counting word occurances
    for word in words:
        if word in dictionary_one_word:
            dictionary_one_word[word] = dictionary_one_word[word] + 1
        else:
            dictionary_one_word[word] = 1
    
    # creating the occurance matrix
    dictionary_one_word = dictionary_one_word.items()
    occurrence_one_matrix = pd.DataFrame(dictionary_one_word)
    occurrence_one_matrix = occurrence_one_matrix.rename(columns={0:"word", 1:"occurance"})
    
    # clean of NaNs
    occurrence_one_matrix = occurrence_one_matrix.loc[occurrence_one_matrix.word.isna() == False, ]
    occurrence_one_matrix = occurrence_one_matrix.loc[occurrence_one_matrix.word != "None", ]

    # sort values
    occurrence_one_matrix = occurrence_one_matrix.sort_values("occurance", ascending=False)

    # re-indexing
    occurrence_one_matrix['index'] = range(len(occurrence_one_matrix))
    occurrence_one_matrix = occurrence_one_matrix.set_index('index')
    return occurrence_one_matrix


def main_script(file_name):
    word_lists(file_name)
    occurrance_three_matrix_creator(file_name)
    occurrance_two_matrix_creator(file_name)
    occurance_one_matrix_creator(file_name)
    print(occurance_one_matrix_creator(file_name))


main_script("testpdf1.pdf")
