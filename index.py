#
# Index file
#
#

# Dependencies
import sys
from downloader import Downloader

# Initialise baseURLs
baseURL = {
    "BNHA" : ("Boku no hero academia", "https://myheromanga.com/"),
    "OPM" : ("One punch man", "https://one-punchmanmanga.com/"),
    "DBS" : ("Dragon ball super", "https://readdragonballsuper.com/")
}

# Check if CLI argument for manga name is passed
if len(sys.argv) > 1 and sys.argv[1] in baseURL.keys():
    # Initialise downloader object
    downloader = Downloader(baseURL[sys.argv[1]])
else:
    print("\nERROR: Missing argument. Mention name of manga to download.\n")
    for key in baseURL.keys():
        print(key, baseURL[key][0])
    print("\n")
    sys.exit()

# Check if CLI argument for chapter limit is passed
if len(sys.argv) > 2:
    downloader.download(int(sys.argv[2]))
else:
    downloader.download()
