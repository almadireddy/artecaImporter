###################################################
# ARTECA supplementary content import preparation #
###################################################

# Aahlad Madireddy
# Run this file outside the folder that contains all the issues
# to go through each issue and all articles in it.

import sys
import os
from bs4 import BeautifulSoup

rootPath = os.path.dirname(sys.argv[1])
print sys.argv
for working, subdirs, files in os.walk(rootPath):
    for subdir in subdirs:
        articleDir = os.path.join(working, subdir)
        supplDir = articleDir + '/suppl'

        # path contains the suppl/ folder, meaning it also contains a .suppl file
        if os.path.isdir(supplDir):
            for w, s, f in os.walk(supplDir):
                for supplFile in os.listdir(articleDir):
                    # find the .suppl file
                    if supplFile.endswith('.suppl'):
                        suppl = open(articleDir + '/' + supplFile)  # open the file
                        soup = BeautifulSoup(suppl, 'html.parser')  # create soup object

                        # find all the <a> tags and make the href
                        # attribute lowercase
                        for a in soup.find_all('a'):
                            hr = a.get('href').lower()
                            a['href'] = hr

                        # get the first href in the suppl file and chop off the filename at the end
                        # this gives us the directory that we need to put the content files in.
                        href = soup.a['href'].split('/')
                        href = href[:-1]
                        href = "/".join(href)

                        # The path we need to create (from os root)
                        completePath = articleDir + "/" + href

                        # check if the directories exist, otherwise, recursively create directories.
                        if os.path.exists(completePath):
                            print "Directory '" + href + "'" + " Already exists"
                        else:
                            os.makedirs(completePath)

                        # for each supplementary file, move that file into the newly created directory
                        for content in os.listdir(w):
                            os.rename(w + "/" + content, completePath + "/" + content)

                        # remove the original suppl/ folder and .suppl file.
                        os.rmdir(w)
                        suppl.close()
                        os.remove(articleDir + '/' + supplFile)

                        # create and save the new .suppl file with the lowercase links.
                        with open(articleDir + '/' + supplFile, 'wb') as writeFile:
                            writeFile.write(soup.prettify('utf-8'))
                            writeFile.close()
