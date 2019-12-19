#
# File to download BNHA manga
#
#

# Dependencies
import requests
import bs4
import os
import sys
import threading

# Set base dir location
location = os.path.join(os.getcwd(), "BNHA")

# Make new dir
if not os.path.exists(location):
    os.makedirs(location)

# Set latest chapter
latestChapter = int(sys.argv[1]) if len(sys.argv)>1 else 2

# Function to get pages for given chapter
def getPages(chapterNo):
    res = requests.get("https://myheromanga.com/manga/boku-no-hero-academia-chapter-"+str(chapterNo))
    # Getting response HTML
    resHTML = bs4.BeautifulSoup(res.text, features="html.parser")

    # Getting only the links
    links = resHTML.select('img[src]')

    # Set chapter dir location
    chapterDir = os.path.join(location, "Chapter "+str(chapterNo))

    # Make new dir for chapter
    if not os.path.exists(chapterDir):
        os.makedirs(chapterDir)

    # Iterate over each image
    for i in range(len(links)):
        # Get image URL
        imageURL = links[i].attrs["src"]

        # Get image from its URL
        image = requests.get(imageURL)

        # Set file name
        filename = "Page "+str(i+1)+".jpeg"

        # Save image to file
        fileObject = open(os.path.join(chapterDir, filename), "wb")
        for chunk in image.iter_content(1024):
            fileObject.write(chunk)
        fileObject.close()

# Thread array
threads = ["Dummy"]

# Iterate over each chapter and Initialise a thread to download chapter
for i in range(1, latestChapter):
    # Initialise threads for each chapter
    threadObj = threading.Thread(target=getPages, args=[i])
    # Append thread to array
    threads.append(threadObj)

# Set active thread limit
activeThreadLimit = 5

# Iterato over all threads
for currentThread in range(1, latestChapter):
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
