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

# Function to get chapters list
def getChapterList():
    # Send request to get list of all chapters
    res = requests.get("https://myheromanga.com/")
    # Parse HTML
    resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
    # Get list containing all chapter numbers
    list = resHTML.select("#Chapters_List a")
    # Reverse list to have first chapter as first element
    list.reverse()
    # Return latest chapter
    return list

# Function to get pages for given chapter
def getPages(chapterNo):
    # res = requests.get("https://myheromanga.com/manga/boku-no-hero-academia-chapter-"+str(chapterNo))
    res = requests.get(chapterList[chapterNo].attrs["href"])
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
    fileObject = open(os.path.join(location, "Chapter "+str(chapterNo+1)+".pdf"), "wb")
    fileObject.write(pdf_bytes)
    fileObject.close()

# Call function to get chapter list
chapterList = getChapterList()

# Set latest chapter search string
latestChapterSearchString = re.compile(r'\d+(\-\d+)?')

# Set latest chapter
latestChapter = int(latestChapterSearchString.search(chapterList[-1].text).group())

# Set chapter limit
chapterLimit = latestChapter

# Check if chapter limit is lesser than latest chapter
if len(sys.argv) > 1 and latestChapter > int(sys.argv[1]):
    chapterLimit = int(sys.argv[1])

# Thread array
threads = []

# Iterate over each chapter and Initialise a thread to download chapter
for i in range(0, chapterLimit):
    # Initialise threads for each chapter
    threadObj = threading.Thread(target=getPages, args=[i])
    # Append thread to array
    threads.append(threadObj)

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
