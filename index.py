#
# Index file
#
#

# Dependencies
import sys, argparse, json
from downloader import Downloader

# Open file to read base URLs
fileObject = open("data.json")
# Initialise base URLs
baseURL = json.load(fileObject)
# Close file object
fileObject.close()

# Initialise a argument parser
parser = argparse.ArgumentParser(prog="manga-downloader")

# Specify arguments
parser.add_argument("manga", nargs="+", choices=[key for key in baseURL.keys()], help="Key value for each manga")
# Initialise a group to add mutually exclusive arguments
group = parser.add_mutually_exclusive_group()
group.add_argument("--trial", action='store_true', help="Flag for trial run")
group.add_argument("--chapterLimit", "-c", type=int, help="Chapter limit")
group.add_argument("--singleChapter", "-s", type=int, help="Chapter number")

# Parse arguments
args = parser.parse_args()

# Check if trial flag was passed
if args.trial:
    for key in args.manga:
        # Initialise downloader object
        downloader = Downloader(baseURL[key])
        # Download first 4 chapters
        downloader.downloadAll(4)
# Check if chapterLimit flag was passed
elif not args.chapterLimit==None:
    for key in args.manga:
        # Initialise downloader object
        downloader = Downloader(baseURL[key])
        # Download first 4 chapters
        downloader.downloadAll(args.chapterLimit)
# Check if chapterLimit flag was passed
elif not args.singleChapter==None:
    for key in args.manga:
        # Initialise downloader object
        downloader = Downloader(baseURL[key])
        # Download first 4 chapters
        downloader.downloadOne(args.singleChapter)
