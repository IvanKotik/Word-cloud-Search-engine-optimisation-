import PyPDF2, re, time, requests, os
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
ps = PorterStemmer()

# This script downloads the full new combined PDF file


# # search terms
# input_initial = 'Pricing and hedging inverse BTC options'
# number_of_urls = 5

# fetching all pdfs
url_text = 'https://raw.githubusercontent.com/IvanKotik/Word-cloud-Search-engine-optimisation-/419447491efef2bb3a21b0459e5bdcd352a39097/combined_pdf_json.json'
r = requests.get(url_text)
combined_pdf = r.json()


# fetching master list
url_master = 'https://raw.githubusercontent.com/IvanKotik/Word-cloud-Search-engine-optimisation-/master/q-master-json.json'
e = requests.get(url_master)
q_master_json = e.json()


# dataframing master list
q_master = pd.DataFrame({'id' : [q_master_json[str(i)]['id'] for i in range(len(q_master_json))],
'name' : [q_master_json[str(i)]['name'] for i in range(len(q_master_json))],
'team' : [q_master_json[str(i)]['team'] for i in range(len(q_master_json))],
'artist' : [q_master_json[str(i)]['artist'] for i in range(len(q_master_json))],
'author' : [q_master_json[str(i)]['author'] for i in range(len(q_master_json))],
'published_in' : [q_master_json[str(i)]['published_in'] for i in range(len(q_master_json))],
'full_link' : [q_master_json[str(i)]['full_link'] for i in range(len(q_master_json))],
'pdf_url' : [q_master_json[str(i)]['pdf_url'] for i in range(len(q_master_json))]
})
q_master['url_check'] = [len(i) for i in q_master['pdf_url']]
q_master = q_master.loc[q_master['url_check'] != 0, ]
q_master = q_master.reset_index(drop=True)


# fetching fresh master
url_fresh_master = 'https://quantinar.com/api/flower/index'
t = requests.get(url_fresh_master)
q_fresh_json = t.json()


# fresh master dataframing
q_check = pd.DataFrame({'id' : [q_fresh_json['data'][i]['id'] for i in range(len(q_fresh_json['data']))],
'name' : [q_fresh_json['data'][i]['name'] for i in range(len(q_fresh_json['data']))],
'team' : [q_fresh_json['data'][i]['team'] for i in range(len(q_fresh_json['data']))],
'artist' : [q_fresh_json['data'][i]['artist'] for i in range(len(q_fresh_json['data']))],
'author' : [q_fresh_json['data'][i]['author'] for i in range(len(q_fresh_json['data']))],
'published_in' : [q_fresh_json['data'][i]['published_in'] for i in range(len(q_fresh_json['data']))],
'full_link' : [q_fresh_json['data'][i]['full_link'] for i in range(len(q_fresh_json['data']))],
'pdf_url' : [q_fresh_json['data'][i]['pdf_url'] for i in range(len(q_fresh_json['data']))]
})
q_check['url_check'] = [len(i) for i in q_check['pdf_url']]
q_check = q_check.loc[q_check['url_check'] != 0, ]
q_check = q_check.reset_index(drop=True)


stopwords_list = {"i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this",'that',"that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"}


def download_pdf(file_name, url):

    '''Download a PDF file with an URL'''

    # Define HTTP Headers
    headers = {"User-Agent": "Chrome/51.0.2704.103"}
    
    # Download image
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    
    # if response is OK download the PDF and store it, else write the status
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)
    
    return


def create_string(file_name, url):
    
    download_pdf(file_name, url)

    '''Transform a PDF file to a list of string pages'''
    
    # opening the file
    imported_pdf = open(file_name, 'rb')
    os.remove(file_name)
    
    # convert PDF to readable file
    transformed_pdf = PyPDF2.PdfFileReader(imported_pdf, strict=False)
    
    # get number of pages
    totalpages = transformed_pdf.numPages
    
    # read the data and store in a list
    pdf_output = [transformed_pdf.getPage(i) for i in range(totalpages)]

    # extract result
    pdf_output = [pdf_output[i].extractText() for i in range(totalpages)]
    
    return pdf_output, totalpages 


def cleaning(file_name, url):

    '''Initial PDF cleaning procedure'''
    
    pdf_output, totalpages = create_string(file_name, url)
    
    # # cleaning URLs
    pdf_output = [re.sub(pattern = "http[^ ]*", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    
    # # cleaning symbols
    pdf_output = [re.sub(pattern = "\\n", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    pdf_output = [re.sub(pattern = "\W|\d", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    pdf_output = [re.sub(pattern = "[^a-zA-Z]", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    
    # # cleaning multispaces
    pdf_output = [re.sub(pattern = "\s{2,}", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    
    # # cleaning out 1-2-worders
    pdf_output = [re.sub(pattern = " .{1,2} ", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    pdf_output = [re.sub(pattern = " .{1,2} ", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    pdf_output = [re.sub(pattern = " .{1,2} ", repl = " ", string = pdf_output[i]) for i in range(totalpages)]
    
    # # lower-casing
    pdf_output = [pdf_output[i].lower() for i in range(totalpages)]
    pdf_output = [[ps.stem(word) for word in sentence.split(" ")] for sentence in pdf_output]
    pdf_output = [' '.join(pdf_output[i]) for i in range(len(pdf_output))]
    
    return pdf_output, totalpages


def combined_pdf_creator():
    '''Creating the final master-pdf dataframe'''

    # clean the first pdf
    pdf_output, totalpages = cleaning(str(q_master.iloc[0, 0]), q_master.iloc[0 ,7])

    # combine the pdf
    combined_pdf = [' '.join(pdf_output)]

    # iterate on above
    for i in range(1, q_master.shape[0]):
        print(i)
        t = time.process_time()
        try:
            pdf_output, totalpages = cleaning(str(q_master.iloc[i, 0]), q_master.iloc[i ,7])
            combined_pdf.append(' '.join(pdf_output))
        except:
            print('problematic file: ', str(q_master.iloc[i, 0]), q_master.iloc[i ,7])
            combined_pdf.append(' '.join(''))
        finally:
            print('time elapsed: ', (time.process_time() - t))
    return combined_pdf


# if triggered, then it means that the pdf downloading must happen again
if all([any(o == q_master['id']) for o in [i for i in q_check['id']]]) == False:
    combined_pdf = combined_pdf_creator()
    try:
        combined_pdf_df = pd.DataFrame({'id' : q_check['id'], "text" : combined_pdf})
        combined_pdf_json = combined_pdf_df.to_json(orient='index')
        with open("combined_pdf_json.json", "w") as outfile:
            outfile.write(combined_pdf_json)
    except: print('problematic file encountered')
else: 
    combined_pdf = [combined_pdf[str(i)]['text'] for i in range(len(combined_pdf))]

