# Set base image
FROM python:3-slim

# Create a python directory
RUN mkdir /home/manga-downloader

# Set workdir
WORKDIR /home/manga-downloader

# Copy code
COPY ./config.json /home/manga-downloader
COPY ./data.json /home/manga-downloader
COPY ./downloader.py /home/manga-downloader
COPY ./index.py /home/manga-downloader
COPY ./README.md /home/manga-downloader
COPY ./requirements.txt /home/manga-downloader

# Install python modules
RUN pip install -r requirements.txt

# Expose volume
VOLUME /mnt

# Set entrypoint
ENTRYPOINT ["python", "index.py"]
