#
# File to download BNHA manga
#
#

# Dependencies
import os
import sys
import threading
import re
import requests
import bs4
import img2pdf

# Set base dir location
location = os.path.join(os.getcwd(), "BNHA")

# Make new dir
if not os.path.exists(location):
    os.makedirs(location)

# Function to get chapters list and latest chapter number
def getChapterList():
    # Send request to get list of all chapters
    res = requests.get("https://myheromanga.com/")
    # Set latest chapter search string
    chapterNoSearchString = re.compile(r'\d+(\.\d+)?')
    # Parse HTML
    resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
    # Get list containing all chapter numbers
    chapterListHTML = resHTML.select("#Chapters_List a")
    # Reverse list to have first chapter as first element
    chapterListHTML.reverse()
    # Get latest chapter
    latestChapter = int(chapterNoSearchString.search(chapterListHTML[-1].text).group())
    # Initialise chapter dict
    chapterList = {}
    # Iteraate over all chapters
    for chapter in chapterListHTML:
        # Append element to chapter list
        chapterList[chapterNoSearchString.search(chapter.text).group()] = chapter.attrs["href"]
    # Return latest chapter
    return [chapterList, latestChapter]

# Function to get pages for given chapter
def getPages(chapterNo):
    # Set chapter file name
    fileName = os.path.join(location, "Chapter "+chapterNo+".pdf")

    # Check if chapter already exists
    if os.path.exists(fileName):
        # Chapter already exists, return
        return

    # Get chapter pages list
    res = requests.get(chapterList[chapterNo])
    # Getting response HTML
    resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
    # Getting only the links
    links = resHTML.select('img[src]')

    # Initialise pages array
    pages = []
    # Iterate over each image
    for currentPage in range(len(links)):
        # Get image URL
        imageURL = links[currentPage].attrs["src"]
        # Get image from its URL
        image = requests.get(imageURL)
        # Append image to pages array
        pages.append(image.content)

    # Convert images into pdf format
    pdf_bytes = img2pdf.convert(pages)
    # Write to pdf
    fileObject = open(fileName, "wb")
    fileObject.write(pdf_bytes)
    fileObject.close()

# Call function to get chapter list
chapterList, latestChapter = getChapterList()

# Set chapter limit
chapterLimit = latestChapter

# Check if chapter limit is lesser than latest chapter
if len(sys.argv) > 1 and latestChapter > int(sys.argv[1]):
    chapterLimit = int(sys.argv[1])

# Thread array
threads = []

# Iterate over each chapter
for key in chapterList.keys():
    # Check if current key is over chapter limit
    if int(round(float(key))) > chapterLimit:
        # Current key is greater than chapter limit
        # Break out of loop
        break;
    else:
        # Initialise threads for each chapter
        threadObj = threading.Thread(target=getPages, args=[key])
        # Append thread to array
        threads.append(threadObj)

# Iterate over each chapter and Initialise a thread to download chapter
# for i in range(0, chapterLimit):
#     # Initialise threads for each chapter
#     threadObj = threading.Thread(target=getPages, args=[i])
#     # Append thread to array
#     threads.append(threadObj)

# Set active thread limit
activeThreadLimit = 5

# Iterato over all threads
for currentThread in range(0, chapterLimit):
    # Check if current thread is under the limit
    if not currentThread > activeThreadLimit:
        # Current thread is under the limit
        # Start current thread
        threads[currentThread].start()
    else:
        # Current thread is over the limit
        # Wait for a thread to finish, then start
        threads[currentThread-activeThreadLimit].join()
        threads[currentThread].start()
