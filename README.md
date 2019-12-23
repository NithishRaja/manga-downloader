# MANGA DOWNLOADER

## Running the script

* run `python index.py <chapter limit>`
* chapter limit is an optional argument
* If no chapter limit is mentioned, all chapters are downloaded

## Editing code

* main code is inside **index.py** file
* download logic is inside **bnha.py** file

## Features

* download chapters till mentioned chapter
* chapter limit must be passed as a CLI argument
* If no CLI argument is passed, all chapters are downloaded
* Code runs five threads at once
* No of threads can be changed by altering the `activeThreadLimit` variable in code
* Each chapter is downloaded as a PDF file
* If a chapter already exists, it is not downloaded again

## Updates

* Check for a new chapter once a week
* Add support for other mangas too
