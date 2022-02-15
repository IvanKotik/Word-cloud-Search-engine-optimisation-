import PyPDF2
import re
import pandas as pd
import numpy as np


file_address = "/Users/ivankotik/Documents/NLP/testpdf2.pdf"
file_location = "/Users/ivankotik/Documents/NLP/"
file_name = "testjson2.json"


def converter_pdf_json_count(file_address, file_location, file_name):
    """
    Count the number of words by occurance in a PDF and export a JSON file with that information
    file_adress example = "/Users/ivankotik/Documents/NLP/testpdf2.pdf"
    file_location example = "/Users/ivankotik/Documents/NLP/"
    file_name example = "testjson2.json"
    """


    # import the file
    imported_pdf = open(file_address, 'rb')

    # transforming the PDF 
    transformed_pdf = PyPDF2.PdfFileReader(imported_pdf)

    # setting the export name 
    file_export = file_location + file_name

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

    # counting the occurances
    for word in words:
        if word in dictionary:
            dictionary[word] = dictionary[word] + 1
        else:
            dictionary[word] = 1

    # transforming the dictionary-counter into a dataframe
    dictionary_words = dictionary.items()
    dictionary_list = list(dictionary_words)
    df_dictionary = pd.DataFrame(dictionary_list)
    df_dictionary = df_dictionary.rename(columns={0:"word", 1:"occurance"})

    # deleting "-"'s seen as words [this part can be extracted based on further data]
    df_dictionary = df_dictionary.drop(df_dictionary[df_dictionary.word == "-"].index)

    # sorting data
    df_dictionary.sort_values("occurance", ascending=False) 

    # counting the word lenght to delete 
    df_dictionary["lenght"] = df_dictionary["word"].apply(lambda x: len(x))
    condition_lenght = df_dictionary["lenght"] > 2

    # fixed dictionary
    df_dictionary_filtered = df_dictionary[condition_lenght]

    # exporting the JSON file 
    df_dictionary_filtered.to_json(file_export)
    print("script executed.")


converter_pdf_json_count("/Users/ivankotik/Documents/NLP/testpdf3.pdf", "/Users/ivankotik/Documents/NLP/", "testjson3.json")