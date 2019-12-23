#
# Index file
#
#

# Dependencies
import sys
from bnha import Downloader

# Initialise downloader object
downloader = Downloader()

# Check if CLI argument is given
if len(sys.argv) > 1:
    downloader.download(int(sys.argv[1]))
else:
    downloader.download()
