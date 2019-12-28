#
# Index file
#
#

# Dependencies
import sys, argparse
from downloader import Downloader

# Initialise baseURLs
baseURL = {
    "BNHA" : ("Boku no hero academia", "https://myheromanga.com/"),
    "OPM" : ("One punch man", "https://one-punchmanmanga.com/"),
    "DBS" : ("Dragon ball super", "https://readdragonballsuper.com/"),
    "DMNSLYR" : ("Demon slayer", "https://demonslayermanga.online/"),
    "HAIKYUU" : ("Haikyuu", "https://haikyuu-manga-online.com/")
}

# Initialise a argument parser
parser = argparse.ArgumentParser(prog="manga-downloader")

# Specify arguments
parser.add_argument("manga", nargs="+", choices=["BNHA", "OPM", "DBS", "DMNSLYR", "HAIKYUU"], help="Key value for each manga")
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
