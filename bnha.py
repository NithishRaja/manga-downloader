#
# File to download BNHA manga
#
#

# Dependencies
import os
import sys
import threading
import re
import time
import requests
import bs4
import img2pdf

# Initialise a state object
state = {
    # Set base dir location
    "location" : os.path.join(os.getcwd(), "BNHA"),
    # Set base URL
    "baseURL" : "https://myheromanga.com/",
    # Set active thread limit
    "activeThreadLimit" : 5,
    # Initialise threads array
    "threads" : [],
    # Initialise latest chapter
    "latestChapter" : 1,
    # Initialise chapter list
    "chapterList" : {},
    #Initialise chapter limit
    "chapterLimit" : 1
}

# Make new dir
if not os.path.exists(state["location"]):
    os.makedirs(state["location"])

# Function to get chapters list and latest chapter number
def getChapterList():
    # Send request to get list of all chapters
    res = requests.get(state["baseURL"])
    # Set latest chapter search string
    chapterNoSearchString = re.compile(r'\d+(\.\d+)?')
    # Parse HTML
    resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
    # Get list containing all chapter numbers
    chapterListHTML = resHTML.select("#Chapters_List a")
    # Reverse list to have first chapter as first element
    chapterListHTML.reverse()
    # Get latest chapter
    state["latestChapter"] = int(chapterNoSearchString.search(chapterListHTML[-1].text).group())
    # Iteraate over all chapters
    for chapter in chapterListHTML:
        # Append element to chapter list
        state["chapterList"][chapterNoSearchString.search(chapter.text).group()] = chapter.attrs["href"]

# Function to get pages for given chapter
def getPages(chapterNo):
    # Set chapter file name
    fileName = os.path.join(state["location"], "Chapter "+chapterNo+".pdf")

    # Check if chapter already exists
    if os.path.exists(fileName):
        # Chapter already exists, return
        return

    # Get chapter pages list
    res = requests.get(state["chapterList"][chapterNo])
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
getChapterList()

# Set chapter limit
state["chapterLimit"] = state["latestChapter"]

# Check if chapter limit is lesser than latest chapter
if len(sys.argv) > 1 and state["latestChapter"] > int(sys.argv[1]):
    state["chapterLimit"] = int(sys.argv[1])

# Iterate over each chapter
for key in state["chapterList"].keys():
    # Check if current key is over chapter limit
    if int(round(float(key))) > state["chapterLimit"]:
        # Current key is greater than chapter limit
        # Break out of loop
        break;
    else:
        # Initialise threads for each chapter
        threadObj = threading.Thread(target=getPages, args=[key])
        # Append thread to array
        state["threads"].append(threadObj)

# Iterate over all threads
for currentThread in state["threads"]:
    # If no of active threads is greater than active thread limit, wait till a thread finishes execution
    while threading.active_count() > state["activeThreadLimit"]:
        # Wait for 3 seconds and check again
        time.sleep(3)
    # Start the thread
    currentThread.start()
