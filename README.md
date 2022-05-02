# Word cloud creator
## Description
This scrip takes in a PDF file like for instance a lecture presentation, cleans it of non-informative data and provides a word cloud of the most used words for the PDF.

## Content
The repo page consists of:
- the Converter.ipynb file that has the description of how the word cloud list iis created;
- Script.py which defines the converter as a function;
- converter.py which runs the script all together and returns a JSON file containing the results:

### Usage of the converter.py

#### 1. Ouput world cloud to file:
```
python3 converter.py "/path/to/pdf/file.pdf  --output=file --filename="/path/to/output.json"
```

#### 2. Ouput world cloud to console:
```
python3 converter.py "/path/to/pdf/file.pdf"  --output=console
```
- couple of test PDF's and JSON's

## Example:
- imput data after conversion to a string
<img width="1345" alt="Screenshot 2022-05-03 at 00 02 19" src="https://user-images.githubusercontent.com/92677707/166335694-af692dbb-b481-46d9-9ed8-bacf6a3c6ba3.png">
- after cleaning the data
<img width="1339" alt="Screenshot 2022-05-03 at 00 02 47" src="https://user-images.githubusercontent.com/92677707/166335782-97639a81-dd87-441d-9155-02e157f19c99.png">
- stopwords
<img width="562" alt="Screenshot 2022-05-03 at 00 03 33" src="https://user-images.githubusercontent.com/92677707/166335804-83ede9c1-3209-4b8d-8cd1-e6ab1420aae7.png">
- words which are left after filtering
<img width="562" alt="Screenshot 2022-05-03 at 00 04 14" src="https://user-images.githubusercontent.com/92677707/166335841-c182a060-60ff-436f-8409-ad75923d9f19.png">
- finalized dataframe
<img width="276" alt="Screenshot 2022-05-03 at 00 04 58" src="https://user-images.githubusercontent.com/92677707/166335861-e03a5c37-01c0-4eca-aece-e8d4d778e2a5.png">


