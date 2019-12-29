#
# File to download BNHA manga
#
#

# Dependencies
import os, threading, re, time
import requests, bs4, img2pdf
from tqdm import tqdm

# Define downloader class
class Downloader:
    # Define init function
    def __init__(this, baseURL, baseDir=os.getcwd()):
        """Initialise variables to default value.

        Keyword arguments:
        baseURL -- a tuple with directory name and manga website url
        """
        # Set the manga name
        this.mangaName = baseURL[0]
        # Set base dir location
        this.baseDir = baseDir
        # Set download location
        this.location = os.path.join(this.baseDir, this.mangaName)
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
        # Set image url attribute
        this.imageURLAttribute = "data-src" if baseURL[0] == "Demon slayer" else "src"

        # Make new dir
        if not os.path.exists(this.location):
            os.makedirs(this.location)

        # Call function to get chapter list
        this.getChapterList()

    # Function to get chapters list and latest chapter number
    def getChapterList(this):
        """Get list of chapters in manga. Fill in missing chapters."""
        # Send request to get list of all chapters
        res = requests.get(this.baseURL)
        # Set latest chapter number search string
        chapterNoSearchString = re.compile(r'\d+(\.\d+)?')
        # Parse HTML
        resHTML = bs4.BeautifulSoup(res.text, features="html.parser")
        # Get list containing all chapter numbers
        chapterListHTML = resHTML.select("#Chapters_List a")
        # Reverse list to have first chapter as first element
        chapterListHTML.reverse()
        # Get latest chapter
        this.latestChapter = int(chapterNoSearchString.search(chapterListHTML[-1].text).group())
        # Checking if chapter list starts from 1
        if not int(chapterNoSearchString.search(chapterListHTML[0].text).group()) == 1:
            # Get lowest chapter number
            lowestChapter = int(chapterNoSearchString.search(chapterListHTML[0].text).group())
            # Initialise chapter URL search string
            chapterURLSearchString = re.compile(r'([a-zA-Z\-\/\.\:]+)')
            # Get chapter URL template
            chapterURLTemplate = chapterURLSearchString.search(chapterListHTML[0].attrs["href"]).group()
            # Iterate over missing chapters and add them to chapterList
            for chapterNo in range(1, lowestChapter):
                # Append element to chapter list
                this.chapterList[str(chapterNo)] = chapterURLTemplate+str(chapterNo)
        # Iteraate over all chapters
        for chapter in chapterListHTML:
            # Append element to chapter list
            this.chapterList[chapterNoSearchString.search(chapter.text).group()] = chapter.attrs["href"]

    # Function to get pages for given chapter
    def getPages(this, chapterNo):
        """Get all pages in given chapter.

        Keyword arguments:
        chapterNo -- string specifying the chapter number
        """
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
        links = resHTML.select('img['+this.imageURLAttribute+']')

        # Initialise pages array
        pages = []
        # Iterate over each image
        for currentPage in tqdm(range(len(links)), desc=this.mangaName+", Chapter "+chapterNo, leave=False, unit="page"):
            # Get image URL
            imageURL = links[currentPage].attrs[this.imageURLAttribute]
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
    def downloadAll(this, chapterLimit):
        """Initialise and start threads to download chapters till chapter limit.

        Keyword arguments:
        chapterLimit -- integer specifying the chapter limit
        """
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

    # Function to begin download
    def downloadOne(this, chapterNo):
        """Initialise and start a thread to download one chapter.

        Keyword arguments:
        chapterNo -- integer specifying the chapter number
        """
        # Check if chapter limit is lesser than latest chapter
        if not type(chapterNo) == int and this.latestChapter > chapterNo:
            print("Given chapter number exceeds the latest chapter")

        # Initialise thread to download chapter
        threadObj = threading.Thread(target=this.getPages, args=[str(chapterNo)])

        # If no of active threads is greater than active thread limit, wait till a thread finishes execution
        while threading.active_count() > this.activeThreadLimit:
            # Wait for 3 seconds and check again
            time.sleep(3)

        # Start thread
        threadObj.start()
