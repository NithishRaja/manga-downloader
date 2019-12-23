#
# File to download BNHA manga
#
#

# Dependencies
import os, threading, re, time
import requests, bs4, img2pdf

# Define downloader class
class Downloader:
    # Define init function
    def __init__(this, baseURL):
        # Set base dir location
        this.location = os.path.join(os.getcwd(), baseURL[0])
        # Set base URL
        this.baseURL = baseURL[1]
        # Set active thread limit
        this.activeThreadLimit = 5
        # Initialise threads array
        this.threads = []
        # Initialise latest chapter
        this.latestChapter = 1
        # Initialise chapter list
        this.chapterList = {}
        #Initialise chapter limit
        this.chapterLimit = 1

        # Make new dir
        if not os.path.exists(this.location):
            os.makedirs(this.location)

        # Call function to get chapter list
        this.getChapterList()

    # Function to get chapters list and latest chapter number
    def getChapterList(this):
        # Send request to get list of all chapters
        res = requests.get(this.baseURL)
        # Set latest chapter search string
        chapterNoSearchString = re.compile(r'\d+(\.\d+)?')
        # Parse HTML
        resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
        # Get list containing all chapter numbers
        chapterListHTML = resHTML.select("#Chapters_List a")
        # Reverse list to have first chapter as first element
        chapterListHTML.reverse()
        # Get latest chapter
        this.latestChapter = int(chapterNoSearchString.search(chapterListHTML[-1].text).group())
        # Iteraate over all chapters
        for chapter in chapterListHTML:
            # Append element to chapter list
            this.chapterList[chapterNoSearchString.search(chapter.text).group()] = chapter.attrs["href"]

    # Function to get pages for given chapter
    def getPages(this, chapterNo):
        # Set chapter file name
        fileName = os.path.join(this.location, "Chapter "+chapterNo+".pdf")

        # Check if chapter already exists
        if os.path.exists(fileName):
            # Chapter already exists, return
            return

        # Get chapter pages list
        res = requests.get(this.chapterList[chapterNo])
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

    # Function to begin download
    def download(this, chapterLimit):
        # Set chapter limit
        this.chapterLimit = this.latestChapter

        # Check if chapter limit is lesser than latest chapter
        if type(chapterLimit) == int and this.latestChapter > chapterLimit:
            this.chapterLimit = chapterLimit

        # Iterate over each chapter
        for key in this.chapterList.keys():
            # Check if current key is over chapter limit
            if int(round(float(key))) > this.chapterLimit:
                # Current key is greater than chapter limit
                # Break out of loop
                break;
            else:
                # Initialise threads for each chapter
                threadObj = threading.Thread(target=this.getPages, args=[key])
                # Append thread to array
                this.threads.append(threadObj)

        # Iterate over all threads
        for currentThread in this.threads:
            # If no of active threads is greater than active thread limit, wait till a thread finishes execution
            while threading.active_count() > this.activeThreadLimit:
                # Wait for 3 seconds and check again
                time.sleep(3)
            # Start the thread
            currentThread.start()
