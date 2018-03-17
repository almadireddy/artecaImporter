# Arteca Supplementary Content Import Prep

## Usage

Simply run the python file in the directory with all the journals, or inside a single issue's directory. 

`python importPrep.py path/to/journal/issue/` 


## Dependencies

You need to have all these dependencies installed and in the path or the local python environment.

- The BeautifulSoup library for parsing html/xml

    `pip install beautifulsoup4`
    
- lxml, to allow BeautifulSoup to parse XML
    
    `pip install lxml`

- The libmagic library, a dependency for python-magic

    `brew install libmagic` on OSX with homebrew

- The python-magic library for file-type detection

    `pip install python-magic`



## Notes

Here is what it does:
- first, find the suppl folder
- if that folder exists, go into the .suppl folder, lowercase all the href attributes, save them into a list
- open up the xml file for that article, to get all the fields for the new xml file
- then create the folder directory according to that href
- move all the files inside suppl/ into that newly created folder
- for all the links, create the appropriate location tags based on file type
- delete suppl/ folder, which was emptied with that move
- write and save the new xml file and the edited .suppl file
