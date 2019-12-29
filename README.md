# MANGA DOWNLOADER

## Running the script

* run `python index.py --help` to view all commands
* the above command also displays the keyword for each manga

### Downloading all chapters

* to download all chapters of given manga, run `python index.py BNHA`
* to download only till a certain chapter, run `python index.py BNHA --chapterLimit 10`

### Downloading only the latest chapter

* run `python index.py BNHA --latestChapter`
* the above command downloads only the chapter of given manga

### Downloading for trial

* run `python index.py BNHA --trial`
* the above command downloads only a few initial chapters
* this can be used to try out a manga without having to download it completely

### Downloading the latest chapter

* run `python index.py BNHA --update`
* the above command downloads only the latest chapter of the manga

### Downloading multiple mangas

* to download multiple mangas at once, run `python index.py BNHA OPM DBS`
* the keyword of each manga should be mentioned one after another before any flags

## Configuration

* Configurations are set in **config.json** file
* No of threads can be changed by altering the `activeThreadLimit` variable
* No of trial chapters can be changed by altering the `trialChapterLimit` variable
* Download location can be changed by altering the `downloadLocation` variable

## Editing code

* main code is inside **index.py** file
* download logic is inside **bnha.py**

## Docker

* docker image can be found at [docker hub](https://hub.docker.com/r/nithishraja/manga-downloader)
* instructions on how to use the image can also be found at [docker hub](https://hub.docker.com/r/nithishraja/manga-downloader)
