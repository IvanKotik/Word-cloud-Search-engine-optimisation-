import PyPDF2
import re
import pandas as pd
import numpy as np


pdf_address = "/Users/ivankotik/Documents/NLP/testpdf2.pdf"
file_location = "/Users/ivankotik/Documents/NLP/testjson2.json"

def converter_pdf_json_count(pdf_address, file_name=""):
    """
    Count the number of words by occurrence in a PDF and export a JSON file with that information
    file_adress example = "/Users/ivankotik/Documents/NLP/testpdf2.pdf"
    file_location example = "/Users/ivankotik/Documents/NLP/"
    file_name example = "testjson2.json"
    """


    # import the file
    imported_pdf = open(pdf_address, 'rb')

    # transforming the PDF 
    transformed_pdf = PyPDF2.PdfFileReader(imported_pdf)

    # initial first page text extraction
    pageObjc_zero = transformed_pdf.getPage(1)
    combined_pages = pageObjc_zero.extractText()

    # initiating cycle for text extraction
    for i in range(2, transformed_pdf.numPages):
        pageObjc_placeholder = transformed_pdf.getPage(i)
        combined_pages = combined_pages + pageObjc_placeholder.extractText()

        combined_pages_w = combined_pages.strip()

    # data cleaning
    combined_pages_w = re.sub(pattern = "\n", repl = "", string = combined_pages_w)
    combined_pages_w = re.sub(pattern = "http[^ ]*", repl = " ", string = combined_pages_w)
    combined_pages_w = re.sub(pattern = "[^\w\-]", repl = " ", string = combined_pages_w)
    combined_pages_w = re.sub(pattern = "\d", repl = " ", string = combined_pages_w)
    combined_pages_w = re.sub(pattern = " +", repl = " ", string = combined_pages_w)
    combined_pages_w = combined_pages_w.lower()

    # creating a dictionary
    dictionary = dict()

    # splitting the string into words
    words = combined_pages_w.split(" ")

    # counting the occurrences
    for word in words:
        if word in dictionary:
            dictionary[word] = dictionary[word] + 1
        else:
            dictionary[word] = 1

    # transforming the dictionary-counter into a dataframe
    dictionary_words = dictionary.items()
    dictionary_list = list(dictionary_words)
    df_dictionary = pd.DataFrame(dictionary_list)
    df_dictionary = df_dictionary.rename(columns={0:"word", 1:"occurrence"})

    # deleting "-"'s seen as words [this part can be extracted based on further data]
    df_dictionary = df_dictionary.drop(df_dictionary[df_dictionary.word == "-"].index)

    # sorting data
    df_dictionary.sort_values("occurrence", ascending=False) 

    # counting the word length to delete 
    df_dictionary["length"] = df_dictionary["word"].apply(lambda x: len(x))
    condition_length = df_dictionary["length"] > 2

    # fixed dictionary
    df_dictionary_filtered = df_dictionary[condition_length]

    # exporting the JSON file
    if file_name == '':
        print(df_dictionary_filtered.to_json(orient='records'))
    else:
        df_dictionary_filtered.to_json(file_name, orient='records')

#converter_pdf_json_count("/Users/wkhaerdle/Documents/Quantlets/NLP/testpdf3.pdf", "/Users/wkhaerdle/Documents/Quantlets/NLP/testjson3.json", output="file")