# Word cloud creator
## Description
This scrip takes in a PDF file like for instance a lecture presentation, cleans it of non-informative data and provides a word cloud of the most used words for the PDF.

## Content
The repo page consists of:
- the Converter.ipynb file that has the description of how the word cloud list iis created;
- Script.py which defines the converter as a function;
- converter.py which runs the script all together and returns a JSON file containing the results:

### Usage of the converter.py

# 1. Ouput world cloud to file:
```
python3 converter.py "/path/to/pdf/file.pdf  --output=file --filename="/path/to/output.json"
```

# 2. Ouput world cloud to console:
```
python3 converter.py "/path/to/pdf/file.pdf"  --output=console
```
- couple of test PDF's and JSON's

## Example:
