###################################################
# ARTECA supplementary content import preparation #
###################################################

# Aahlad Madireddy
# Run this file outside the folder that contains all the issues
# to go through each issue and all articles in it.
# brew install libmagic before running (for filetype detection)

import sys
import os
import magic
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
                        contentLinks = list()

                        for a in soup.find_all('a'):
                            hr = a.get('href').lower()
                            a['href'] = hr
                            contentLinks.append(hr)

                        # get the first href in the suppl file and chop off the filename at the end
                        # this gives us the directory that we need to put the content files in.
                        href = soup.a['href'].split('/')
                        articleCode = href[4]
                        href = href[:-1]
                        href = "/".join(href)

                        originalXml = open(articleDir + '/' + articleCode + '.xml')
                        newXml = open(articleDir + '/' + articleCode + '.suppl.xml', 'wb')
                        xSoup = BeautifulSoup(originalXml, 'xml')

                        docType = xSoup.article['dtd-version']
                        journalId = xSoup.select('journal-id[journal-id-type="publisher-id"]')[0].extract()

                        if docType == '3.0':
                            journalTitle = xSoup.find('journal-title-group').extract()
                        else:
                            journalTitle = xSoup.select('abbrev-journal-title[abbrev-type="full"]')[0].extract()

                        publisherName = xSoup.find('publisher-name').extract()
                        articleId = xSoup.select('article-id[pub-id-type="doi"]')[0].extract()
                        articleTitle = xSoup.find('title-group').extract()

                        xSoup.front.clear()
                        xSoup.front.append(xSoup.new_tag('journal-meta'))
                        xSoup.find('journal-meta').append(journalId)
                        xSoup.find('journal-meta').append(journalTitle)
                        xSoup.find('journal-meta').append(xSoup.new_tag('publisher'))
                        xSoup.find('publisher').append(publisherName)

                        xSoup.front.append(xSoup.new_tag('article-meta'))
                        xSoup.find('article-meta').append(articleId)
                        xSoup.find('article-meta').append(articleTitle)
                        xSoup.find('article-meta').append(xSoup.new_tag('abstract'))
                        xSoup.find('article-meta').append(xSoup.new_tag('location-group'))

                        # The path we need to create (from os root)
                        completePath = articleDir + "/" + href

                        print "Currently processing: " + supplFile

                        # check if the directories exist, otherwise, recursively create directories.
                        if os.path.exists(completePath):
                            print "Directory '" + href + "'" + " Already exists"
                        else:
                            os.makedirs(completePath)

                        # for each supplementary file, move that file into the newly created directory
                        for content in os.listdir(w):
                            os.rename(w + "/" + content, completePath + "/" + content)

                        for link in contentLinks:
                            try:
                                fileType = magic.from_file(articleDir + link, mime=True)
                            except IOError as e:
                                continue

                            if fileType.startswith("audio"):
                                tag = xSoup.new_tag('audio')
                                tag.append(link)
                                xSoup.find('location-group').append(tag)

                            elif fileType.startswith("video"):
                                tag = xSoup.new_tag('video')
                                tag.append(link)
                                xSoup.find('location-group').append(tag)

                            elif fileType.startswith("image"):
                                tag = xSoup.new_tag('image')
                                tag.append(link)
                                xSoup.find('location-group').append(tag)

                            else:
                                tag = xSoup.new_tag('audio')
                                tag.append(link)
                                xSoup.find('location-group').append(tag)

                        newXml.write(str(xSoup))

                        # remove the original suppl/ folder and .suppl file.
                        os.rmdir(w)
                        suppl.close()
                        os.remove(articleDir + '/' + supplFile)
                        newXml.close()

                        # create and save the new .suppl file with the lowercase links.
                        with open(articleDir + '/' + supplFile, 'wb') as writeFile:
                            writeFile.write(soup.prettify('utf-8'))
                            writeFile.close()
