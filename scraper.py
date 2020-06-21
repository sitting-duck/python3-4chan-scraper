import sys
import os
import requests
from re import sub, finditer
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import ntpath 

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_board_threads(url):

    thread_ids = []
    # Get URLs of all active threads of a board
    # I understand that this code is very hacked together
    # the while loop reads from an identifiable section of
    # the HTML backwards to the end of each thread ID.
    # BeautifulSoup cannot work with this because the respose
    # is actually a JSON object (I belive)
    html = requests.get(url).text
    #print("mah html" + str(html.encode()))

    # '":{"date"' is the only unique pattern found near each thread ID
    indicies = [x.start() for x in finditer('":{"date"', html)]
    for indice in indicies:
        thread_id = ""
        counter = 1
        while html[indice-counter] != '"':
            thread_id = html[indice-counter] + thread_id
            counter += 1
        thread_ids.append(thread_id)
    print(thread_ids)
    for thread in thread_ids:
        print("thread: " + str(thread))

    # Omit the first post, because it's always a
    # mod's sticky for the board
    return thread_ids[1:]


def download_file(url, dest_dir, filename=None):
    print("download_file():")
    print("url: " + str(url))
    print("dest_dir: " + str(dest_dir))
    print("filename: " + str(filename))

    # If no specific filename is provided, use the filename as
    # exists on the URL path
    if(filename is None):
        #filename = urlsplit(url).path.split("/")[-1]
        print("mah url: " + str(url))
        filename = path_leaf(url)

    request = requests.get(url)
    image = Image.open(BytesIO(request.content))
    image.save(os.path.join(dest_dir, filename))


def get_file_urls(soup):
    print("get_file_urls(): ")
    for item in soup:
        print("item: " + str(item.encode()))

    file_urls = []

    for anchor in soup.find_all(attrs={'class': 'fileThumb'}):
        print("mah anchor: " + str(anchor))
        print("mah anchor type: " +str( type(anchor)))
        # Fix 4chan's href, which excludes the 'https://' protocol
        file_urls.append(sub("//", "http://", str(anchor.get('href'))))

    return file_urls


def get_filenames(soup):
    filenames = []

    for anchor in soup.find_all(attrs={'class': 'fileText'}):
        filenames.append(anchor.get_text().split(" ")[1])

    return filenames


def main():

    print("4chan Image Scraper by Grayson Pike")

    if(sys.argv[1] == "thread"):
        # First argument is the thread URL
        url = sys.argv[2]
        # Second is the output directory
        # Output directory is via local (relative) path
        # ex. output
        # ex. output/
        # You can also do absolute paths (only tested with linux & mac)
        # ex. /Users/graysonpike/Desktop/4chan
        dest_dir = sys.argv[3]

        print("Downloading images from " + url + " ...")
        html = requests.get(url).text
        # Beautiful soup allows for easy document navigation
        soup = BeautifulSoup(html, "html.parser")

        file_urls = get_file_urls(soup)
        filenames = get_filenames(soup)

        for i in range(len(file_urls)):
            print("Downloading File: " + filenames[i])
            download_file(file_urls[i], dest_dir, filenames[i])

    elif(sys.argv[1] == "board"):
        board = sys.argv[2]
        print("Checking board catalog @: " + "http://boards.4chan.org/" + board + "/catalog")
        #board_url = "http://boards.4chan.org/" + board + "/catalog"
        board_url = "http://boards.4chan.org/" + board
        thread_ids = get_board_threads(board_url)
        dest_dir = sys.argv[3]

        for thread in thread_ids:
            print("Downloading thread (id: " + thread + ") @: http://boards.4chan.org/" + board + "/thread/" + thread)
            url = "http://boards.4chan.org/" + board + "/thread/" + thread
            html = requests.get(url).text

            # Beautiful soup allows for easy document navigation
            soup = BeautifulSoup(html, "html.parser")
            file_urls = get_file_urls(soup)
            filenames = get_filenames(soup)
            for i in range(len(file_urls)):
                print("mah i: " + str(i))
                print("len fn: " + str(len(filenames)) + " " + str(len(file_urls)))
                #download_file(file_urls[i], dest_dir, filenames[i])
                download_file(file_urls[i], dest_dir)

    else:
        print("Usage: python3 scraper.py <'thread' or 'board'> <thread url or board letter> <dest directory>")
        print("See: https://github.com/Grayson112233/python-4chan-scraper")


main()
