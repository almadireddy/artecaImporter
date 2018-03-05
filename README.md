# Arteca Supplementary Content Import Prep

## Usage

Simply run the python file in the directory with all the journals, or inside a single issue's directory. 

`python importPrep.py path/to/journal/issue/` 

You need to have BeautifulSoup installed and in the path or environment (for parsing html/xml) 

`pip install beautifulsoup4`

## Notes

Here is what it does:
- first, find the suppl folder
- if that folder exists, go into the .suppl folder, lowercase all the href attributes 
- then create the folder directory according to that href
- move all the files inside suppl/ into that newly created folder
- delete suppl/ folder, which was emptied with that move. 
